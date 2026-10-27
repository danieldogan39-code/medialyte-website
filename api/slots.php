<?php
/**
 * GET /api/slots.php – liefert bereits vergebene Termine, damit das Formular sie ausblendet.
 * Enthält bewusst keine personenbezogenen Daten.
 */
declare(strict_types=1);
require __DIR__ . '/lib.php';

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'GET') {
    header('Allow: GET');
    ml_json(405, ['ok' => false]);
}
ml_json(200, ['ok' => true, 'booked' => ml_booked_slots()]);
