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
        'smtp_host'         => 'smtp.ionos.de',
        'smtp_port'         => 587,
        'smtp_user'         => '',   // leer = Absenderadresse (termine@medialyte.de)
        'smtp_pass'         => '',   // gesetzt = Versand über SMTP statt mail()
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

/** Geheimer Schlüssel für die Begrenzung, einmal zufällig erzeugt und nur auf dem Server gespeichert. */
function ml_secret(): string
{
    $file = ml_data_dir() . '/secret.key';
    if (!is_file($file)) {
        @file_put_contents($file, bin2hex(random_bytes(32)), LOCK_EX);
        @chmod($file, 0600);
    }
    return (string) @file_get_contents($file);
}

/** Einfache Begrenzung pro IP: gespeichert nur als HMAC mit geheimem Schlüssel, nie im Klartext. */
function ml_rate_limited(): bool
{
    $file = ml_data_dir() . '/ratelimit.json';
    $key = hash_hmac('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . date('Y-m-d'), ml_secret());
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

/** Letzter Versandfehler (ohne Adressen), für das Protokoll. */
$GLOBALS['ml_mail_error'] = '';

/**
 * E-Mail versenden. Ist in config.php ein SMTP-Passwort hinterlegt, geht die Mail angemeldet über den
 * IONOS-Mailserver (zuverlässig, mit SPF/DKIM des Postfachs). Sonst über PHP mail() des Webspace.
 */
function ml_mail(string $to, string $subject, string $text, ?string $ics = null, ?string $replyTo = null): bool
{
    $cfg = ml_config();
    $GLOBALS['ml_mail_error'] = '';
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
    $subj = mb_encode_mimeheader($subject, 'UTF-8');
    if (!empty($cfg['smtp_pass'])) {
        return ml_smtp($to, $subj, $headers, $body);
    }
    $ok = @mail($to, $subj, $body, implode("\r\n", $headers), '-f' . $cfg['mail_from']);
    if (!$ok) {
        $GLOBALS['ml_mail_error'] = 'mail() abgelehnt';
    }
    return $ok;
}

/** Schlanker SMTP-Versand mit STARTTLS und Anmeldung (IONOS: smtp.ionos.de, Port 587). */
function ml_smtp(string $to, string $subject, array $headers, string $body): bool
{
    $cfg = ml_config();
    $fail = function (string $why) use (&$fp): bool {
        $GLOBALS['ml_mail_error'] = 'SMTP: ' . $why;
        if (is_resource($fp)) {
            @fwrite($fp, "QUIT\r\n");
            @fclose($fp);
        }
        return false;
    };
    $fp = @stream_socket_client('tcp://' . $cfg['smtp_host'] . ':' . (int) $cfg['smtp_port'], $errno, $errstr, 15);
    if (!$fp) {
        return $fail("keine Verbindung ($errno)");
    }
    stream_set_timeout($fp, 15);
    $read = function () use ($fp): string {
        $all = '';
        while (($line = fgets($fp, 1024)) !== false) {
            $all .= $line;
            if (strlen($line) < 4 || $line[3] !== '-') {
                break;
            }
        }
        return $all;
    };
    $cmd = function (string $c, string $expect) use ($fp, $read): bool {
        if ($c !== '') {
            fwrite($fp, $c . "\r\n");
        }
        return strncmp($read(), $expect, 3) === 0;
    };
    $host = parse_url($cfg['allowed_origins'][0] ?? 'https://medialyte.de', PHP_URL_HOST) ?: 'medialyte.de';
    if (!$cmd('', '220')) return $fail('Begrüßung');
    if (!$cmd('EHLO ' . $host, '250')) return $fail('EHLO');
    if (!$cmd('STARTTLS', '220')) return $fail('STARTTLS');
    if (!@stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT | (defined('STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT') ? STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT : 0))) return $fail('TLS');
    if (!$cmd('EHLO ' . $host, '250')) return $fail('EHLO nach TLS');
    if (!$cmd('AUTH LOGIN', '334')) return $fail('AUTH');
    if (!$cmd(base64_encode($cfg['smtp_user'] ?: $cfg['mail_from']), '334')) return $fail('Benutzer');
    if (!$cmd(base64_encode($cfg['smtp_pass']), '235')) return $fail('Anmeldung abgelehnt (Passwort prüfen)');
    if (!$cmd('MAIL FROM:<' . $cfg['mail_from'] . '>', '250')) return $fail('Absender abgelehnt');
    if (!$cmd('RCPT TO:<' . $to . '>', '250')) return $fail('Empfänger abgelehnt');
    if (!$cmd('DATA', '354')) return $fail('DATA');
    $all = array_merge([
        'Date: ' . date('r'),
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . $host . '>',
        'To: ' . $to,
        'Subject: ' . $subject,
    ], $headers);
    $msg = implode("\r\n", $all) . "\r\n\r\n" . preg_replace("/\r?\n/", "\r\n", $body);
    $msg = preg_replace('/^\./m', '..', $msg);   // Punkt am Zeilenanfang verdoppeln (SMTP)
    if (!$cmd($msg . "\r\n.", '250')) return $fail('Nachricht abgelehnt');
    @fwrite($fp, "QUIT\r\n");
    @fclose($fp);
    return true;
}

/** Versandprotokoll ohne Inhalte und ohne Adressen (nur zur Fehlersuche): Zeit, Anfrage, Empfängerart, Ergebnis, Grund. */
function ml_log_mail(string $id, string $to, bool $ok): void
{
    $why = $ok ? '' : "\t" . ($GLOBALS['ml_mail_error'] ?? '');
    @file_put_contents(ml_data_dir() . '/mail.log', date('c') . "\t" . $id . "\t" . $to . "\t" . ($ok ? 'ok' : 'FEHLER') . $why . "\n", FILE_APPEND | LOCK_EX);
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
    $loc = $b['format'] === 'vor-ort' ? 'Bei Ihnen vor Ort (Adresse stimmen wir vorher ab)' : $b['format_text'];
    return implode("\r\n", [
        'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Medialyte//Termin//DE', 'METHOD:PUBLISH', 'BEGIN:VEVENT',
        'UID:' . $b['id'] . '@medialyte.de', 'DTSTAMP:' . $f(new DateTime('now', $tz)),
        'DTSTART:' . $f($start), 'DTEND:' . $f($end),
        'SUMMARY:Erstgespräch mit Medialyte', 'DESCRIPTION:' . $b['format_text'] . ' – Ihr Ansprechpartner: Daniel',
        'LOCATION:' . $loc, 'END:VEVENT', 'END:VCALENDAR',
    ]);
}
