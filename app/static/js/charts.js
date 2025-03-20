document.addEventListener('DOMContentLoaded', function() {
    // Equipment Health Distribution Chart
    const healthChartElem = document.getElementById('equipment-health-chart');
    if (healthChartElem) {
        const data = JSON.parse(healthChartElem.getAttribute('data-stats'));
        new Chart(healthChartElem, {
            type: 'doughnut',
            data: {
                labels: ['Healthy', 'Warning', 'Critical'],
                datasets: [{
                    data: [data.healthy_percent, data.warning_percent, data.critical_percent],
                    backgroundColor: ['#28a745', '#ffc107', '#dc3545'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed.toFixed(1)}%`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    }

    // Maintenance Status Chart
    const maintenanceChartElem = document.getElementById('maintenance-status-chart');
    if (maintenanceChartElem) {
        const data = JSON.parse(maintenanceChartElem.getAttribute('data-stats'));
        new Chart(maintenanceChartElem, {
            type: 'bar',
            data: {
                labels: ['Scheduled', 'In Progress', 'Completed', 'Cancelled'],
                datasets: [{
                    label: 'Maintenance Tasks',
                    data: [data.scheduled, data.in_progress, data.completed, data.cancelled || 0],
                    backgroundColor: [
                        'rgba(255, 193, 7, 0.7)',
                        'rgba(23, 162, 184, 0.7)',
                        'rgba(40, 167, 69, 0.7)',
                        'rgba(108, 117, 125, 0.7)'
                    ],
                    borderColor: [
                        'rgb(255, 193, 7)',
                        'rgb(23, 162, 184)',
                        'rgb(40, 167, 69)',
                        'rgb(108, 117, 125)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

    // Equipment Health History Chart
    const healthHistoryChart = document.getElementById('equipment-health-history');
    if (healthHistoryChart) {
        const historyData = JSON.parse(healthHistoryChart.getAttribute('data-history'));
        new Chart(healthHistoryChart, {
            type: 'line',
            data: {
                labels: historyData.dates,
                datasets: [{
                    label: 'Health Score',
                    data: historyData.scores,
                    borderColor: function(context) {
                        const value = context.raw;
                        if (value >= 70) return '#28a745';
                        else if (value >= 60) return '#ffc107';
                        else return '#dc3545';
                    },
                    fill: false,
                    tension: 0.1,
                    pointBackgroundColor: function(context) {
                        const value = context.raw;
                        if (value >= 70) return '#28a745';
                        else if (value >= 60) return '#ffc107';
                        else return '#dc3545';
                    }
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Health: ${context.parsed.y}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Health Score (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                },
                animation: {
                    duration: 2000
                }
            }
        });
    }

    // User Roles Distribution Chart
    const userRolesChartElem = document.getElementById('user-roles-chart');
    if (userRolesChartElem) {
        const userData = JSON.parse(userRolesChartElem.getAttribute('data-stats'));
        new Chart(userRolesChartElem, {
            type: 'pie',
            data: {
                labels: ['Boss', 'Admin', 'Engineer'],
                datasets: [{
                    data: [userData.boss, userData.admin, userData.engineer],
                    backgroundColor: ['#007bff', '#17a2b8', '#28a745'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    }
    
    // Update charts when theme changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'data-bs-theme') {
                Chart.getChart('equipment-health-chart')?.update();
                Chart.getChart('maintenance-status-chart')?.update();
                Chart.getChart('equipment-health-history')?.update();
                Chart.getChart('user-roles-chart')?.update();
            }
        });
    });
    
    observer.observe(document.documentElement, { attributes: true });
}); 