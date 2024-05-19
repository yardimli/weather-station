<?php
header('Content-Type: application/json');

// Include the configuration
$config = include('config.php');

// Create connection
$conn = new mysqli($config['servername'], $config['username'], $config['password'], $config['dbname']);

// Check connection
if ($conn->connect_error) {
    die(json_encode(array("error" => "Connection failed: " . $conn->connect_error)));
}

// Check if the POST data exists
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Retrieve the data
    $id = $_POST['id'];
    $ambient_temperature = $_POST['ambient_temperature'];
    $ground_temperature = $_POST['ground_temperature'];
    $air_quality = $_POST['air_quality'];
    $air_pressure = $_POST['air_pressure'];
    $humidity = $_POST['humidity'];
    $wind_direction = $_POST['wind_direction'];
    $wind_speed = $_POST['wind_speed'];
    $wind_gust_speed = $_POST['wind_gust_speed'];
    $rainfall = $_POST['rainfall'];
    $created = $_POST['created']; // Assumes datetime

    // Insert query to save the data in the database
    $sql = "INSERT INTO ". $config['tablename'] ." (remote_id, ambient_temperature, ground_temperature, air_quality, air_pressure, humidity, wind_direction, wind_speed, wind_gust_speed, rainfall, created)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

    $stmt = $conn->prepare($sql);

    if ($stmt) {
        // Bind parameters
        $stmt->bind_param("sssssssssss", $id, $ambient_temperature, $ground_temperature, $air_quality, $air_pressure, $humidity, $wind_direction, $wind_speed, $wind_gust_speed, $rainfall, $created);

        // Execute the statement
        if ($stmt->execute()) {
            // Retrieve the last inserted id
            $save_id = $stmt->insert_id;
            echo json_encode(array("save_id" => $save_id));
        } else {
            echo json_encode(array("error" => "Failed to insert data: " . $stmt->error));
        }

        // Close the statement
        $stmt->close();
    } else {
        echo json_encode(array("error" => "Failed to prepare statement: " . $conn->error));
    }
} else {
    echo json_encode(array("error" => "Invalid request method"));
}

// Close the connection
$conn->close();