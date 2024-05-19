<?php
	session_start();
	include_once 'config.php';
	?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<title>Pi Weather</title>

	<!-- FAVICON AND TOUCH ICONS -->
	<link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon">
	<link rel="icon" href="images/favicon.ico" type="image/x-icon">
	<link rel="apple-touch-icon" sizes="152x152" href="images/apple-touch-icon-152x152.png">
	<link rel="apple-touch-icon" sizes="120x120" href="images/apple-touch-icon-120x120.png">
	<link rel="apple-touch-icon" sizes="76x76" href="images/apple-touch-icon-76x76.png">
	<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
	<link rel="icon" href="images/apple-touch-icon.png" type="image/x-icon">

	<!-- Bootstrap CSS -->
	<link href="css/bootstrap.min.css" rel="stylesheet">
	<!-- Custom styles for this template -->
	<link href="css/custom.css" rel="stylesheet"> <!-- If you have custom CSS -->
	<meta name="csrf-token" content="{{ csrf_token() }}">

	<script>
	</script>
</head>
<body>
<header>
	<!-- Bootstrap Navbar or custom header content here -->
</header>

<main class="py-4">
	<div class="container mt-2">
		<h1 style="margin:10px;" class="text-center"><img src="images/android-chrome-192x192.png" style="height: 64px;"> Pi Weather</h1>

		<!-- Canvas for chart -->
		<canvas id="weatherChart" class="weather-chart"></canvas>
		
		<table class="table table-bordered table-hover" id="data-table">
			<thead>
			<tr>
				<th scope="col" data-sort="id">ID</th>
				<th scope="col" data-sort="ambient_temperature">Ambient Temperature</th>
				<th scope="col" data-sort="ground_temperature">Ground Temperature</th>
				<th scope="col" data-sort="air_quality">Air Quality</th>
				<th scope="col" data-sort="air_pressure">Air Pressure</th>
				<th scope="col" data-sort="humidity">Humidity</th>
				<th scope="col" data-sort="wind_direction">Wind Direction</th>
				<th scope="col" data-sort="wind_speed">Wind Speed</th>
				<th scope="col" data-sort="wind_gust_speed">Wind Gust Speed</th>
				<th scope="col" data-sort="rainfall">Rainfall</th>
				<th scope="col" data-sort="created">Created</th>
			</tr>
			</thead>
			<tbody>
			<!-- Data will be appended here by jQuery -->
			</tbody>
		</table>
		<nav>
			<ul class="pagination">
				<!-- Pagination will be appended here by jQuery -->
			</ul>
		</nav>

	</div>
</main>

<footer>
	<!-- Bootstrap footer or custom footer content here -->
</footer>

<!-- Bootstrap JS, Popper.js, and jQuery -->
<script src="js/jquery-3.7.0.min.js"></script>
<script src="js/bootstrap.min.js"></script>

<!-- Chart.js -->
<script src="js/chart.js"></script>
<script src="js/moment.min.js"></script>
<script src="js/chartjs-adapter-moment.js"></script>
<script src="js/chartjs-plugin-datalabels.min.js"></script>


<!-- Custom JS -->
<script src="js/custom.js"></script>

</body>

</html>
