<?php
require_once('vendor/autoload.php');

$client = new MongoDB\Client("mongodb://mongodb:27017");
$collection = $client->iot_data->sensor_data;

echo "<h2>🌿 MongoDB: sensor_data Collection</h2>";

$cursor = $collection->find([], ['sort' => ['_id' => -1]]);

echo "<table border='1'><tr><th>Topic</th><th>Value</th></tr>";
foreach ($cursor as $doc) {
    $topic = $doc['topic'] ?? 'N/A';
    $value = is_array($doc['value']) ? json_encode($doc['value']) : $doc['value'];
    echo "<tr><td>{$topic}</td><td>{$value}</td></tr>";
}
echo "</table>";
?>
