<?php
	header('Content-Type: application/json');

	$config = include('config.php');

// Create connection
	$conn = new mysqli($config['servername'], $config['username'], $config['password'], $config['dbname']);

// Check connection
	if ($conn->connect_error) {
		die(json_encode(array("error" => "Connection failed: " . $conn->connect_error)));
	}

	$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
	$limit = 50;
	$offset = ($page - 1) * $limit;
	$sortField = isset($_GET['sortField']) ? $_GET['sortField'] : 'created';
	$sortOrder = isset($_GET['sortOrder']) ? $_GET['sortOrder'] : 'desc';

// Fetch total records
	$totalQuery = "SELECT COUNT(*) AS total FROM ". $config['tablename'];
	$totalResult = $conn->query($totalQuery);
	$totalRow = $totalResult->fetch_assoc();
	$totalRecords = $totalRow['total'];
	$totalPages = ceil($totalRecords / $limit);

// Fetch data with pagination and sorting
	$query = "SELECT * FROM ". $config['tablename'] ." ORDER BY $sortField $sortOrder LIMIT $limit OFFSET $offset";
	$result = $conn->query($query);

	$data = array();
	if ($result->num_rows > 0) {
		while ($row = $result->fetch_assoc()) {
			$data[] = $row;
		}
	}

	echo json_encode(array(
		"data" => $data,
		"totalPages" => $totalPages
	));

	$conn->close();
