<?php
/**
 * Medialyte – gemeinsame Funktionen für Terminbuchung und Slots.
 * Läuft auf jedem IONOS-Webhosting mit PHP 8.1 oder neuer.
 */
declare(strict_types=1);

function ml_config(): array
{
    static $cfg = null;
    if ($cfg !== null) {
        return $cfg;
    }
    $defaults = [
        'mail_to'           => 'info@medialyte.de',
        'mail_from'         => 'termine@medialyte.de',
        'mail_from_name'    => 'Medialyte',
        'send_confirmation' => true,
        'webhook_url'       => '',   // Endpunkt des Medialyte-Dashboards
        'webhook_secret'    => '',   // gemeinsamer Schlüssel für die HMAC-Signatur
        'data_dir'          => __DIR__ . '/data',
        'allowed_origins'   => ['https://medialyte.de', 'https://www.medialyte.de'],
        'duration'          => 30,
        'days_ahead'        => 60,
        'hours'             => [1 => ['09:00', '18:00'], 2 => ['09:00', '18:00'], 3 => ['09:00', '18:00'], 4 => ['09:00', '18:00'], 5 => ['09:00', '16:00']],
        'rate_limit'        => 5,    // Buchungen pro IP und Stunde
        'timezone'          => 'Europe/Berlin',
    ];
    $file = __DIR__ . '/config.php';
    $cfg = is_file($file) ? array_replace($defaults, (array) require $file) : $defaults;
    date_default_timezone_set($cfg['timezone']);
    return $cfg;
}

function ml_json(int $status, array $body): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($body, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

function ml_data_dir(): string
{
    $dir = ml_config()['data_dir'];
    if (!is_dir($dir)) {
        mkdir($dir, 0750, true);
    }
    $ht = $dir . '/.htaccess';
    if (!is_file($ht)) {
        file_put_contents($ht, "<IfModule mod_authz_core.c>\n  Require all denied\n</IfModule>\n<IfModule !mod_authz_core.c>\n  Deny from all\n</IfModule>\n");
    }
    return $dir;
}

/** Text säubern: Steuerzeichen raus, Länge begrenzen. */
function ml_clean($value, int $max = 300): string
{
    if (!is_scalar($value)) {
        return '';
    }
    $s = trim((string) $value);
    $s = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $s) ?? '';
    return mb_substr($s, 0, $max);
}

function ml_check_origin(): void
{
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    if ($origin !== '' && !in_array(rtrim($origin, '/'), ml_config()['allowed_origins'], true)) {
        ml_json(403, ['ok' => false, 'error' => 'Anfrage nicht erlaubt.']);
    }
}

/** Einfache Begrenzung pro IP (gespeichert als Hash, nicht als Klartext). */
function ml_rate_limited(): bool
{
    $file = ml_data_dir() . '/ratelimit.json';
    $key = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . date('Y-m-d'));
    $now = time();
    $fh = fopen($file, 'c+');
    if (!$fh) {
        return false;
    }
    flock($fh, LOCK_EX);
    $data = json_decode(stream_get_contents($fh) ?: '{}', true) ?: [];
    foreach ($data as $k => $times) {
        $data[$k] = array_values(array_filter($times, fn($t) => $t > $now - 3600));
        if (!$data[$k]) {
            unset($data[$k]);
        }
    }
    $limited = count($data[$key] ?? []) >= (int) ml_config()['rate_limit'];
    if (!$limited) {
        $data[$key][] = $now;
    }
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, json_encode($data));
    flock($fh, LOCK_UN);
    fclose($fh);
    return $limited;
}

/** Alle gespeicherten Buchungen lesen. */
function ml_bookings(): array
{
    $file = ml_data_dir() . '/bookings.jsonl';
    if (!is_file($file)) {
        return [];
    }
    $out = [];
    foreach (file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $row = json_decode($line, true);
        if (is_array($row)) {
            $out[] = $row;
        }
    }
    return $out;
}

/** Belegte Termine im Format YYYY-MM-DDTHH:MM (ohne personenbezogene Daten). */
function ml_booked_slots(): array
{
    $today = date('Y-m-d');
    $slots = [];
    foreach (ml_bookings() as $b) {
        $t = $b['termin'] ?? null;
        if (!$t || ($b['status'] ?? 'neu') === 'storniert') {
            continue;
        }
        if (($t['datum'] ?? '') >= $today) {
            $slots[] = $t['datum'] . 'T' . $t['uhrzeit'];
        }
    }
    return array_values(array_unique($slots));
}

/** Prüft, ob ein Termin grundsätzlich buchbar ist (Arbeitstag, Uhrzeit, Zukunft). */
function ml_slot_valid(string $date, string $time): bool
{
    $cfg = ml_config();
    if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $date) || !preg_match('/^\d{2}:\d{2}$/', $time)) {
        return false;
    }
    $dt = DateTime::createFromFormat('Y-m-d H:i', "$date $time", new DateTimeZone($cfg['timezone']));
    if (!$dt) {
        return false;
    }
    $now = new DateTime('now', new DateTimeZone($cfg['timezone']));
    if ($dt <= $now || $dt > (clone $now)->modify('+' . (int) $cfg['days_ahead'] . ' days')) {
        return false;
    }
    $dow = (int) $dt->format('N');
    if (empty($cfg['hours'][$dow])) {
        return false;
    }
    [$from, $to] = $cfg['hours'][$dow];
    $end = (clone $dt)->modify('+' . (int) $cfg['duration'] . ' minutes')->format('H:i');
    return $time >= $from && $end <= $to;
}

function ml_mail(string $to, string $subject, string $text, ?string $ics = null, ?string $replyTo = null): bool
{
    $cfg = ml_config();
    $from = sprintf('%s <%s>', mb_encode_mimeheader($cfg['mail_from_name'], 'UTF-8'), $cfg['mail_from']);
    $headers = ['From: ' . $from, 'MIME-Version: 1.0'];
    if ($replyTo) {
        $headers[] = 'Reply-To: ' . $replyTo;
    }
    if ($ics) {
        $b = 'ml-' . bin2hex(random_bytes(8));
        $headers[] = 'Content-Type: multipart/mixed; boundary="' . $b . '"';
        $body = "--$b\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n$text\r\n"
              . "--$b\r\nContent-Type: text/calendar; charset=UTF-8; method=PUBLISH; name=\"medialyte-termin.ics\"\r\n"
              . "Content-Disposition: attachment; filename=\"medialyte-termin.ics\"\r\nContent-Transfer-Encoding: 8bit\r\n\r\n$ics\r\n--$b--";
    } else {
        $headers[] = 'Content-Type: text/plain; charset=UTF-8';
        $headers[] = 'Content-Transfer-Encoding: 8bit';
        $body = $text;
    }
    return @mail($to, mb_encode_mimeheader($subject, 'UTF-8'), $body, implode("\r\n", $headers), '-f' . $cfg['mail_from']);
}

/** Buchung signiert an das Dashboard weitergeben. Fehler blockieren die Buchung nicht. */
function ml_webhook(array $payload): bool
{
    $cfg = ml_config();
    if (empty($cfg['webhook_url'])) {
        return false;
    }
    $body = json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    $sig = 'sha256=' . hash_hmac('sha256', $body, (string) $cfg['webhook_secret']);
    $headers = ['Content-Type: application/json', 'X-Medialyte-Signature: ' . $sig, 'X-Medialyte-Event: booking.created'];
    if (function_exists('curl_init')) {
        $ch = curl_init($cfg['webhook_url']);
        curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $body, CURLOPT_HTTPHEADER => $headers,
            CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 6, CURLOPT_CONNECTTIMEOUT => 4]);
        curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        return $code >= 200 && $code < 300;
    }
    $ctx = stream_context_create(['http' => ['method' => 'POST', 'header' => implode("\r\n", $headers), 'content' => $body, 'timeout' => 6, 'ignore_errors' => true]]);
    return @file_get_contents($cfg['webhook_url'], false, $ctx) !== false;
}

/** Datum auf Deutsch, auch ohne intl-Erweiterung: „Donnerstag, 30. Oktober 2026“. */
function ml_date_de(string $ymd): string
{
    $tage = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
    $monate = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
    $d = DateTime::createFromFormat('Y-m-d', $ymd);
    return $d ? $tage[(int) $d->format('w')] . ', ' . (int) $d->format('j') . '. ' . $monate[(int) $d->format('n') - 1] . ' ' . $d->format('Y') : $ymd;
}

function ml_ics(array $b): string
{
    $cfg = ml_config();
    $tz = new DateTimeZone($cfg['timezone']);
    $start = DateTime::createFromFormat('Y-m-d H:i', $b['termin']['datum'] . ' ' . $b['termin']['uhrzeit'], $tz);
    $end = (clone $start)->modify('+' . (int) $cfg['duration'] . ' minutes');
    $utc = new DateTimeZone('UTC');
    $f = fn(DateTime $d) => (clone $d)->setTimezone($utc)->format('Ymd\THis\Z');
    $loc = $b['format'] === 'vor-ort' ? 'Medialyte, Schaaphusen 3, 21147 Hamburg' : $b['format_text'];
    return implode("\r\n", [
        'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Medialyte//Termin//DE', 'METHOD:PUBLISH', 'BEGIN:VEVENT',
        'UID:' . $b['id'] . '@medialyte.de', 'DTSTAMP:' . $f(new DateTime('now', $tz)),
        'DTSTART:' . $f($start), 'DTEND:' . $f($end),
        'SUMMARY:Erstgespräch mit Medialyte', 'DESCRIPTION:' . $b['format_text'] . ' – Ihr Ansprechpartner: Daniel',
        'LOCATION:' . $loc, 'END:VEVENT', 'END:VCALENDAR',
    ]);
}
