<?php
/**
 * Kopieren als api/config.php auf dem Server (wird nicht ins Repository übernommen)
 * und die Werte anpassen. Nicht gesetzte Werte nehmen die Standards aus lib.php.
 */
return [
    'mail_to'           => 'info@medialyte.de',
    'mail_from'         => 'termine@medialyte.de',   // Postfach/Adresse muss bei IONOS existieren
    'mail_from_name'    => 'Medialyte',
    'send_confirmation' => true,

    // Anbindung an das Medialyte-Dashboard
    'webhook_url'       => '',   // z. B. https://cockpit.medialyte.de/api/leads
    'webhook_secret'    => '',   // langer Zufallswert, identisch im Dashboard hinterlegen

    // Verfügbarkeit (1 = Montag … 5 = Freitag), muss zu BOOKING in build.py passen
    'hours' => [1 => ['09:00', '18:00'], 2 => ['09:00', '18:00'], 3 => ['09:00', '18:00'], 4 => ['09:00', '18:00'], 5 => ['09:00', '16:00']],
    'duration'   => 30,
    'days_ahead' => 60,
];
