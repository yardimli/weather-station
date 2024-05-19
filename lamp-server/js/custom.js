$(document).ready(function () {
	let currentPage = 1;
	let sortField = 'created';
	let sortOrder = 'desc';
	let weatherChart;
	
	function fetchData(page, sortField, sortOrder) {
		$.ajax({
			url: 'fetch_data.php',
			type: 'GET',
			data: {
				page: page,
				sortField: sortField,
				sortOrder: sortOrder
			},
			dataType: 'json',
			success: function (response) {
				if (response.data.length) {
					let tableRows = '';
					let labels = [];
					let ambientTemp = [], groundTemp = [], airQuality = [], airPressure = [], humidity = [], windDirection = [],
						windSpeed = [], windGustSpeed = [], rainfall = [];
					
					response.data.forEach(function (item) {
						tableRows += `<tr>
                            <td>${item.REMOTE_ID}</td>
                            <td>${item.AMBIENT_TEMPERATURE}</td>
                            <td>${item.GROUND_TEMPERATURE}</td>
                            <td>${item.AIR_QUALITY}</td>
                            <td>${item.AIR_PRESSURE}</td>
                            <td>${item.HUMIDITY}</td>
                            <td>${item.WIND_DIRECTION}</td>
                            <td>${item.WIND_SPEED}</td>
                            <td>${item.WIND_GUST_SPEED}</td>
                            <td>${item.RAINFALL}</td>
                            <td>${item.CREATED}</td>
                        </tr>`;
						
						labels.push(item.CREATED);
						ambientTemp.push(item.AMBIENT_TEMPERATURE);
						groundTemp.push(item.GROUND_TEMPERATURE);
						airQuality.push(item.AIR_QUALITY);
						airPressure.push(item.AIR_PRESSURE);
						humidity.push(item.HUMIDITY);
						windDirection.push(item.WIND_DIRECTION);
						windSpeed.push(item.WIND_SPEED);
						windGustSpeed.push(item.WIND_GUST_SPEED);
						rainfall.push(item.RAINFALL);
					});
					$('#data-table tbody').html(tableRows);
					
					let paginationControls = '';
					for (let i = 1; i <= response.totalPages; i++) {
						paginationControls += `<li class="page-item ${i === page ? 'active' : ''}">
                            <a class="page-link" href="#" data-page="${i}">${i}</a>
                        </li>`;
					}
					$('.pagination').html(paginationControls);
					
					// Update the chart
					if (weatherChart) {
						weatherChart.destroy();
					}
					const ctx = document.getElementById('weatherChart').getContext('2d');
					weatherChart = new Chart(ctx, {
						type: 'line',
						data: {
							labels: labels,
							datasets: [{
								label: 'Ambient Temperature',
								data: ambientTemp,
								borderColor: 'rgba(255, 99, 132, 1)',
								fill: false
							}, {
								label: 'Ground Temperature',
								data: groundTemp,
								borderColor: 'rgba(54, 162, 235, 1)',
								fill: false
							}, {
								label: 'Air Quality',
								data: airQuality,
								borderColor: 'rgba(255, 206, 86, 1)',
								fill: false
							}, {
								label: 'Air Pressure',
								data: airPressure,
								borderColor: 'rgba(75, 192, 192, 1)',
								fill: false
							}, {
								label: 'Humidity',
								data: humidity,
								borderColor: 'rgba(153, 102, 255, 1)',
								fill: false
							}, {
								label: 'Wind Direction',
								data: windDirection,
								borderColor: 'rgba(255, 159, 64, 1)',
								fill: false
							}, {
								label: 'Wind Speed',
								data: windSpeed,
								borderColor: 'rgba(100, 99, 132, 1)',
								fill: false
							}, {
								label: 'Wind Gust Speed',
								data: windGustSpeed,
								borderColor: 'rgba(200, 162, 235, 1)',
								fill: false
							}, {
								label: 'Rainfall',
								data: rainfall,
								borderColor: 'rgba(150, 159, 64, 1)',
								fill: false
							}]
						},
						options: {
							responsive: true,
							scales: {
								x: {
									type: 'time',
									time: {
										unit: 'second'
									}
								},
								y: {
									beginAtZero: true
								}
							}
						}
					});
				} else {
					$('#data-table tbody').html('<tr><td colspan="11" class="text-center">No data available</td></tr>');
				}
			},
			error: function (error) {
				console.error('Error fetching data:', error);
			}
		});
	}
	
	function init() {
		fetchData(currentPage, sortField, sortOrder);
		
		$('.pagination').on('click', '.page-link', function (e) {
			e.preventDefault();
			currentPage = $(this).data('page');
			fetchData(currentPage, sortField, sortOrder);
		});
		
		$('#data-table th').on('click', function () {
			sortField = $(this).data('sort');
			sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
			fetchData(currentPage, sortField, sortOrder);
		});
	}
	
	init();
});
