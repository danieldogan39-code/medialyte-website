<?php
/**
 * POST /api/termin.php – nimmt eine Terminanfrage aus dem Buchungsformular entgegen.
 * Speichert sie, prüft auf Doppelbuchung, informiert Medialyte und den Kunden per E-Mail
 * und leitet sie signiert an das Medialyte-Dashboard weiter.
 */
declare(strict_types=1);
require __DIR__ . '/lib.php';

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    ml_json(405, ['ok' => false, 'error' => 'Nur POST erlaubt.']);
}
ml_check_origin();

$raw = file_get_contents('php://input', false, null, 0, 20000) ?: '';
$in = json_decode($raw, true);
if (!is_array($in)) {
    ml_json(400, ['ok' => false, 'error' => 'Ungültige Anfrage.']);
}

// Verstecktes Feld: Bots füllen es aus. Browser mit automatischem Ausfüllen manchmal auch –
// deshalb wird nichts verworfen: Die Anfrage geht als „Bitte prüfen“ an Medialyte, nur ohne Bestätigung an den Absender.
$spam = ml_clean($in['hp'] ?? '') !== '';
if (ml_rate_limited()) {
    ml_json(429, ['ok' => false, 'error' => 'Zu viele Anfragen. Bitte versuchen Sie es später erneut oder schreiben Sie uns per WhatsApp.']);
}

$allowedAnliegen = ['web-neu', 'web-besser', 'system', 'werbung', 'agent', 'brief'];
$formats = ['video' => 'Video-Call', 'telefon' => 'Telefon', 'vor-ort' => 'Vor Ort bei Ihnen'];

$b = [
    'id'            => date('Ymd-His') . '-' . bin2hex(random_bytes(3)),
    'erstellt'      => date('c'),
    'status'        => 'neu',
    'anliegen'      => array_values(array_intersect($allowedAnliegen, array_map('strval', (array) ($in['anliegen'] ?? [])))),
    'anliegen_text' => array_map(fn($s) => ml_clean($s, 80), array_slice((array) ($in['anliegen_text'] ?? []), 0, 6)),
    'firma'         => ml_clean($in['firma'] ?? '', 150),
    'branche'       => ml_clean($in['branche'] ?? '', 80),
    'website'       => ml_clean($in['website'] ?? '', 200),
    'ort'           => ml_clean($in['ort'] ?? '', 80),
    'groesse'       => ml_clean($in['groesse'] ?? '', 20),
    'format'        => array_key_exists($in['format'] ?? '', $formats) ? $in['format'] : '',
    'name'          => ml_clean($in['name'] ?? '', 120),
    'email'         => ml_clean($in['email'] ?? '', 160),
    'telefon'       => ml_clean($in['telefon'] ?? '', 40),
    'whatsapp_ok'   => !empty($in['whatsapp_ok']),
    'nachricht'     => ml_clean($in['nachricht'] ?? '', 3000),
    'einwilligung'  => !empty($in['einwilligung']),
    'quelle'        => [
        'seite'    => ml_clean($in['quelle']['seite'] ?? '', 120),
        'referrer' => ml_clean($in['quelle']['referrer'] ?? '', 300),
        'utm'      => array_map(fn($s) => ml_clean($s, 120), (array) ($in['quelle']['utm'] ?? [])),
    ],
    'termin'   => null,
    'rueckruf' => null,
    'pruefen'  => $spam,
];
$b['format_text'] = $formats[$b['format']] ?? '';

// Pflichtfelder
$errors = [];
if (!$b['anliegen']) $errors[] = 'Anliegen';
if ($b['firma'] === '') $errors[] = 'Unternehmen';
if ($b['format'] === '') $errors[] = 'Gesprächsart';
if (mb_strlen($b['name']) < 2) $errors[] = 'Name';
if (!filter_var($b['email'], FILTER_VALIDATE_EMAIL)) $errors[] = 'E-Mail';
if (!$b['einwilligung']) $errors[] = 'Einwilligung';

if (!empty($in['rueckruf'])) {
    $zf = ml_clean($in['rueckruf']['zeitfenster'] ?? 'flexibel', 20);
    $b['rueckruf'] = ['zeitfenster' => in_array($zf, ['vormittags', 'nachmittags', 'flexibel'], true) ? $zf : 'flexibel'];
    if (strlen(preg_replace('/\D/', '', $b['telefon'])) < 6) $errors[] = 'Telefon';
} else {
    $datum = ml_clean($in['termin']['datum'] ?? '', 10);
    $zeit = ml_clean($in['termin']['uhrzeit'] ?? '', 5);
    if (!ml_slot_valid($datum, $zeit)) {
        $errors[] = 'Termin';
    } else {
        $b['termin'] = ['datum' => $datum, 'uhrzeit' => $zeit, 'dauer_min' => (int) ml_config()['duration'],
                        'start' => (new DateTime("$datum $zeit"))->format('c')];
    }
    if ($b['format'] === 'telefon' && strlen(preg_replace('/\D/', '', $b['telefon'])) < 6) $errors[] = 'Telefon';
}
if ($errors) {
    ml_json(422, ['ok' => false, 'error' => 'Bitte prüfen Sie: ' . implode(', ', $errors) . '.']);
}

// Speichern mit Sperre, damit kein Termin doppelt vergeben wird
$file = ml_data_dir() . '/bookings.jsonl';
$fh = fopen($file, 'c+');
if (!$fh) {
    ml_json(500, ['ok' => false, 'error' => 'Speichern nicht möglich. Bitte schreiben Sie uns per WhatsApp.']);
}
flock($fh, LOCK_EX);
if ($b['termin']) {
    $key = $b['termin']['datum'] . 'T' . $b['termin']['uhrzeit'];
    if (in_array($key, ml_booked_slots(), true)) {
        flock($fh, LOCK_UN);
        fclose($fh);
        ml_json(409, ['ok' => false, 'error' => 'Dieser Termin wurde gerade vergeben.']);
    }
}
fseek($fh, 0, SEEK_END);
fwrite($fh, json_encode($b, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n");
fflush($fh);
flock($fh, LOCK_UN);
fclose($fh);

// Texte für die E-Mails
$wann = $b['termin']
    ? ml_date_de($b['termin']['datum']) . ', ' . $b['termin']['uhrzeit'] . ' Uhr (' . $b['format_text'] . ')'
    : 'Rückruf gewünscht (' . $b['rueckruf']['zeitfenster'] . ')';
$lines = [
    'Neue Terminanfrage über medialyte.de', '',
    'Termin:      ' . $wann,
    'Anliegen:    ' . implode(', ', $b['anliegen_text'] ?: $b['anliegen']),
    'Unternehmen: ' . $b['firma'] . ($b['branche'] ? ' (' . $b['branche'] . ')' : ''),
    'Website:     ' . ($b['website'] ?: '–'),
    'Ort:         ' . ($b['ort'] ?: '–'),
    'Größe:       ' . ($b['groesse'] ?: '–'),
    'Name:        ' . $b['name'],
    'E-Mail:      ' . $b['email'],
    'Telefon:     ' . ($b['telefon'] ?: '–') . ($b['whatsapp_ok'] ? ' (WhatsApp-Bestätigung gewünscht)' : ''),
    '', 'Nachricht:', $b['nachricht'] ?: '–', '',
    'Quelle: ' . $b['quelle']['seite'] . ($b['quelle']['referrer'] ? ' über ' . $b['quelle']['referrer'] : ''),
    'ID: ' . $b['id'],
];
$sentTeam = ml_mail(ml_config()['mail_to'], ($spam ? '[Bitte prüfen] ' : '') . 'Neue Terminanfrage: ' . $b['firma'], implode("\n", $lines), $b['termin'] ? ml_ics($b) : null, $b['email']);
ml_log_mail($b['id'], 'Medialyte', $sentTeam);

if (ml_config()['send_confirmation'] && !$spam) {
    $vorname = explode(' ', $b['name'])[0];
    $confirm = [
        "Hallo $vorname,", '',
        'vielen Dank für Ihre Anfrage. Wir haben Folgendes für Sie notiert:', '',
        $wann, 'Anliegen: ' . implode(', ', $b['anliegen_text'] ?: $b['anliegen']), '',
        $b['termin'] ? 'Den Termin finden Sie im Anhang zum Eintragen in Ihren Kalender. Wir melden uns vorher, falls sich etwas ändert.' : 'Wir rufen Sie im gewünschten Zeitfenster an.',
        '', 'Sie möchten etwas ändern? Antworten Sie einfach auf diese E-Mail oder schreiben Sie uns per WhatsApp: https://wa.me/491709647532',
        '', 'Viele Grüße', 'Daniel', 'Medialyte – Marketing & Management', 'medialyte.de',
    ];
    $sentCustomer = ml_mail($b['email'], 'Ihr Termin mit Medialyte', implode("\n", $confirm), $b['termin'] ? ml_ics($b) : null, ml_config()['mail_to']);
    ml_log_mail($b['id'], 'Bestätigung', $sentCustomer);
}

ml_webhook($b);
ml_json(200, ['ok' => true, 'id' => $b['id']]);
