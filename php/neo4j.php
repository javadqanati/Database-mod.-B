<?php
require_once 'vendor/autoload.php';

use Laudis\Neo4j\ClientBuilder;

$client = ClientBuilder::create()
    ->withDriver('bolt', 'bolt://neo4j:test1234@neo4j:7687')
    ->build();

echo "<h2>🧠 Neo4j: Device Nodes</h2>";

$result = $client->run('
MATCH (u:User)-[:OWNS]->(d:Device)-[r:REPORTS]->(s:Sensor)
RETURN u.name AS user, d.name AS device, d.sensor AS sensor, 
       r.reading AS reading, r.status AS status, r.timestamp AS timestamp, s.type AS sensorType
');


foreach ($result as $record) {
    echo "User: " . $record->get('user') . "<br>";
    echo "Device: " . $record->get('device') . "<br>";
    echo "Sensor: " . $record->get('sensor') . "<br>";
    echo "Sensor Type: " . $record->get('sensorType') . "<br>";
    echo "Reading: " . $record->get('reading') . "<br>";
    echo "Status: " . $record->get('status') . "<br>";
    echo "Timestamp: " . $record->get('timestamp') . "<hr>";
}


?>
