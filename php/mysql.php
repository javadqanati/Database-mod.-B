<?php
$servername = "mysql";
$username = "root";
$password = "1234test";
$database = "iot_data";

$conn = new mysqli($servername, $username, $password, $database);

if ($conn->connect_error) {
    die("❌ Connection failed: " . $conn->connect_error);
}

$sql = "SELECT topic, value, timestamp FROM temperature_data ORDER BY timestamp DESC";
$result = $conn->query($sql);

echo "<h2>🌡️ MySQL: temperature_data Table</h2>";

if ($result->num_rows > 0) {
    echo "<table border='1'><tr><th>#</th><th>Topic</th><th>Value</th><th>Timestamp</th></tr>";
    $count = 1;
    while($row = $result->fetch_assoc()) {
        echo "<tr><td>$count</td><td>{$row["topic"]}</td><td>{$row["value"]}</td><td>{$row["timestamp"]}</td></tr>";
        $count++;
    }
    echo "</table>";
} else {
    echo "No data found.";
}

$conn->close();
?>
