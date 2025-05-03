// Update time and date
function updateDateTime() {
    const now = new Date();

    // Update time
    const timeElement = document.getElementById('time');
    timeElement.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Update date
    const dateElement = document.getElementById('date');
    const options = { weekday: 'long', month: 'long', day: 'numeric' };
    dateElement.textContent = now.toLocaleDateString(undefined, options);
}

// Run initially and set interval
updateDateTime();
setInterval(updateDateTime, 60000); // Update every minute

// Function to update curtain position
function updateCurtainPosition(value) {
    // Update UI
    curtainValue.textContent = value;
    console.log(`Curtains set to ${value}%`);
    
    // Send request to server
    fetch(`/curtain/set/${value}`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
        throw new Error('Failed to set curtain position');
        }
        return response.json();
    })
    .then(data => {
        console.log('Curtain position updated successfully:', data);
    })
    .catch(error => {
        console.error('Error updating curtain position:', error);
    });
}

// Handle the curtain slider
const curtainSlider = document.getElementById('curtainSlider');
const curtainValue = document.getElementById('curtainValue');
if (curtainSlider) {
    curtainSlider.addEventListener('input', function () {
        updateCurtainPosition(this.value);
    });
}

// Add event listeners for the curtain preset buttons
document.querySelectorAll('.preset-btn').forEach(button => {
    button.addEventListener('click', function () {
        const value = this.getAttribute('data-value');
        const curtainSlider = document.getElementById('curtainSlider');
        
        curtainSlider.value = value;
        updateCurtainPosition(value);
    });
});

// Initialize the dashboard when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Initialize charts if Chart.js is loaded
    if (typeof Chart !== 'undefined') {
        setupCurtainStatusChart();
        fetchCurtainData('20min'); 
        setupTemperatureChart();
        fetchTemperatureData('20min'); 
        setupHumidityChart(); 
        fetchHumidityData('20min');
        setupLightChart();
        fetchLightData('20min');
    }
    // Initialize the curtain slider and value display
    const curtainSlider = document.getElementById('curtainSlider');
    const curtainValue = document.getElementById('curtainValue');
    if (curtainSlider) {
        fetch('/curtain/get')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch curtain position');
                }
                return response.json();
            })
            .then(data => {
                curtainSlider.value = data.curtain_pos;
                curtainValue.textContent = data.curtain_pos;
                console.log(`Curtain position fetched: ${data.curtain_pos}%`);
            })
            .catch(error => {
                console.error('Error fetching curtain position:', error);
            });
    }
});

////////////////////////////////////////////////////////////////////////////////////////////////////////
//Graph Section 
////////////////////////////////////////////////////////////////////////////////////////////////////////
// Handle the temperature time range toggles
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('overlay-checkbox') && 
        (event.target.id === 'tempToday' || event.target.id === 'tempHour' || event.target.id === 'temp20Min')) {
        
        // If the clicked checkbox was already checked, keep it checked
        if (!event.target.checked) {
            event.target.checked = true;
            return;
        }
        
        // Get all temperature checkboxes
        const tempCheckboxes = document.querySelectorAll('#tempToday, #tempHour, #temp20Min');
        
        // Uncheck all other checkboxes
        tempCheckboxes.forEach(checkbox => {
            if (checkbox !== event.target) {
                checkbox.checked = false;
            }
        });
        
        // Fetch data based on the selected time range
        let timeRange;
        switch (event.target.id) {
            case 'tempToday':
                timeRange = 'today';
                break;
            case 'tempHour':
                timeRange = 'hour';
                break;
            case 'temp20Min':
                timeRange = '20min';
                break;
        }
        
        if (timeRange) {
            fetchTemperatureData(timeRange);
        }
    }
});

// Handle the time range toggles for humidity
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('overlay-checkbox') &&
        (event.target.id === 'humToday' || event.target.id === 'humHour' || event.target.id === 'hum20Min')) {

        // If the clicked checkbox was already checked, keep it checked
        if (!event.target.checked) {
            event.target.checked = true;
            return;
        }

        // Get all humidity checkboxes
        const humidityCheckboxes = document.querySelectorAll('#humToday, #humHour, #hum20Min');

        // Uncheck all other checkboxes
        humidityCheckboxes.forEach(checkbox => {
            if (checkbox !== event.target) {
                checkbox.checked = false;
            }
        });

        // Fetch data based on the selected time range
        let timeRange;
        switch (event.target.id) {
            case 'humToday':
                timeRange = 'today';
                break;
            case 'humHour':
                timeRange = 'hour';
                break;
            case 'hum20Min':
                timeRange = '20min';
                break;
        }

        if (timeRange) {
            fetchHumidityData(timeRange);
        }
    }
});

// Handle the time range toggles for humidity
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('overlay-checkbox') &&
        (event.target.id === 'curToday' || event.target.id === 'curHour' || event.target.id === 'cur20Min')) {

        // If the clicked checkbox was already checked, keep it checked
        if (!event.target.checked) {
            event.target.checked = true;
            return;
        }

        // Get all humidity checkboxes
        const humidityCheckboxes = document.querySelectorAll('#curToday, #curHour, #cur20Min');

        // Uncheck all other checkboxes
        humidityCheckboxes.forEach(checkbox => {
            if (checkbox !== event.target) {
                checkbox.checked = false;
            }
        });

        // Fetch data based on the selected time range
        let timeRange;
        switch (event.target.id) {
            case 'curToday':
                timeRange = 'today';
                break;
            case 'curHour':
                timeRange = 'hour';
                break;
            case 'cur20Min':
                timeRange = '20min';
                break;
        }

        if (timeRange) {
            fetchCurtainData(timeRange);
        }
    }
});

// Handle the time range toggles for light levels
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('overlay-checkbox') &&
        (event.target.id === 'lightToday' || event.target.id === 'lightHour' || event.target.id === 'light20Min')) {

        // If the clicked checkbox was already checked, keep it checked
        if (!event.target.checked) {
            event.target.checked = true;
            return;
        }

        // Get all light checkboxes
        const lightCheckboxes = document.querySelectorAll('#lightToday, #lightHour, #light20Min');

        // Uncheck all other checkboxes
        lightCheckboxes.forEach(checkbox => {
            if (checkbox !== event.target) {
                checkbox.checked = false;
            }
        });

        // Fetch data based on the selected time range
        let timeRange;
        switch (event.target.id) {
            case 'lightToday':
                timeRange = 'today';
                break;
            case 'lightHour':
                timeRange = 'hour';
                break;
            case 'light20Min':
                timeRange = '20min';
                break;
        }

        if (timeRange) {
            fetchLightData(timeRange);
        }
    }
});

////////////////////////////////////////////////////////////////////////////////////////////////////////

// Setup the curtain status chart (similar to temperature and humidity chart)
function setupCurtainStatusChart() {
    const ctx = document.getElementById('curtainStatusChart');
    if (!ctx) return;

    window.curtainStatusChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Curtain Position',
                data: [],
                borderColor: 'rgba(52, 152, 219, 1)', // Light blue color
                backgroundColor: 'rgba(52, 152, 219, 0.1)', // Light fill color
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointStyle: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Position: ${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    min: -20,
                    max: 100,
                    ticks: {
                        callback: function (value) {
                            return value + '%';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Curtain Position (%)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 4,
                        // Use time-based labels
                        callback: function(value, index, ticks) {
                            // If labels are already formatted as time strings, use them directly
                            time = window.curtainStatusChart.data.labels[index];
                            // If time is in 12-hour format (like "2:30 PM"), convert to 24-hour format
                            if (time && time.includes(':')) {
                                // Check if it's already in the format we need
                                if (time.includes(' ')) {
                                    const [timePart, meridiem] = time.split(' ');
                                    const [hour, minute] = timePart.split(':').map(Number);
                                    
                                    // Convert to 24-hour format
                                    let hour24 = hour;
                                    if (meridiem === 'PM' && hour < 12) hour24 += 12;
                                    if (meridiem === 'AM' && hour === 12) hour24 = 0;
                                    
                                    time = `${hour24.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
                                }
                            }
                            return time || value;
                        }
                    }
                }
            }
        }
    });
}

// Fetch curtain status data from the API
async function fetchCurtainData(timeRange) {
    try {
        const response = await fetch(`/curtain/${timeRange}`);
        if (!response.ok) throw new Error("Failed to fetch curtain data");
        const data = await response.json();

        // Extract timestamps and curtain position values
        let labels = data.map(entry => entry.timestamp);
        const curtainPositions = data.map(entry => entry.curtain_pos);

        // Convert numeric indices to time labels if needed
        if (labels.length > 0 && typeof labels[0] === 'number') {
            const now = new Date();
            const minutes = timeRange.includes('min') ? parseInt(timeRange) : 60;
            const interval = minutes / labels.length;

            // Create time labels working backward from now
            labels = labels.map((_, index) => {
                const time = new Date(now.getTime() - (labels.length - 1 - index) * interval * 60000);
                return time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            });
        }

        // Update the curtain status chart with the new data
        updateCurtainChart(labels, curtainPositions);
        console.log(`Fetched curtain data for ${timeRange}:`, labels, curtainPositions);
    } catch (error) {
        console.error("Error fetching curtain data:", error);
    }
}

// Update curtain status chart with fetched data
function updateCurtainChart(labels, curtainPositions) {
    if (window.curtainStatusChart) {
        window.curtainStatusChart.data.labels = labels;
        window.curtainStatusChart.data.datasets[0].data = curtainPositions;
        window.curtainStatusChart.update();
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////
async function fetchTemperatureData(timeRange) {
    try {
        const response = await fetch(`/temp/${timeRange}`);
        if (!response.ok) throw new Error("Failed to fetch data");
        const data = await response.json();
        
        // Extract timestamps and temperature values
        let labels = data.map(entry => entry.timestamp);
        const temperatures = data.map(entry => entry.temperature);
        
        // Convert numeric indices to time labels if needed
        if (labels.length > 0 && typeof labels[0] === 'number') {
            // If timestamps are just numeric indices, create time-based labels
            const now = new Date();
            const minutes = timeRange.includes('min') ? parseInt(timeRange) : 60;
            const interval = minutes / labels.length;
            
            // Create time labels working backward from now
            labels = labels.map((_, index) => {
                const time = new Date(now.getTime() - (labels.length - 1 - index) * interval * 60000);
                return time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            });
        }
        
      
        
        updateTemperatureChart(labels, temperatures);
    } catch (error) {
        console.error("Error fetching temperature data:", error);
    }
}

function setupTemperatureChart() {
    const ctx = document.getElementById('temperatureChart');
    if (!ctx) return;
    
    window.temperatureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Indoor Temperature',
                data: [],
                borderColor: 'rgba(231, 76, 60, 1)',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointStyle: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Temperature: ${context.parsed.y}°C`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        callback: function (value) {
                            return value + '°C';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 5,
                        // For direct display of the labels without parsing
                        callback: function(value, index, ticks) {
                            // If labels are already formatted as time strings, use them directly
                            time = window.temperatureChart.data.labels[index];
                            // If time is in 12-hour format (like "2:30 PM"), convert to 24-hour format
                            if (time && time.includes(':')) {
                                // Check if it's already in the format we need
                                if (time.includes(' ')) {
                                    const [timePart, meridiem] = time.split(' ');
                                    const [hour, minute] = timePart.split(':').map(Number);
                                    
                                    // Convert to 24-hour format
                                    let hour24 = hour;
                                    if (meridiem === 'PM' && hour < 12) hour24 += 12;
                                    if (meridiem === 'AM' && hour === 12) hour24 = 0;
                                    
                                    time = `${hour24.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
                                }
                            }
                            return time || value;
                        }
                    }
                }
            }
        }
    });
}

function updateTemperatureChart(labels, temperatures) {
    if (window.temperatureChart) {
        window.temperatureChart.data.labels = labels;
        window.temperatureChart.data.datasets[0].data = temperatures;
        window.temperatureChart.update();
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////
function setupHumidityChart() {
    const ctx = document.getElementById('humidityChart');
    if (!ctx) return;

    window.humidityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Indoor Humidity',
                data: [],
                borderColor: 'rgba(52, 152, 219, 1)', // Light blue color
                backgroundColor: 'rgba(52, 152, 219, 0.1)', // Light fill color
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointStyle: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Humidity: ${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        callback: function (value) {
                            return value + '%';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Humidity (%)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 5,
                        // If labels are time-based, format them properly
                        callback: function(value, index, ticks) {
                            // If labels are already formatted as time strings, use them directly
                            time = window.temperatureChart.data.labels[index];
                            // If time is in 12-hour format (like "2:30 PM"), convert to 24-hour format
                            if (time && time.includes(':')) {
                                // Check if it's already in the format we need
                                if (time.includes(' ')) {
                                    const [timePart, meridiem] = time.split(' ');
                                    const [hour, minute] = timePart.split(':').map(Number);
                                    
                                    // Convert to 24-hour format
                                    let hour24 = hour;
                                    if (meridiem === 'PM' && hour < 12) hour24 += 12;
                                    if (meridiem === 'AM' && hour === 12) hour24 = 0;
                                    
                                    time = `${hour24.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
                                }
                            }
                            return time || value;
                        }
                    }
                }
            }
        }
    });
}

async function fetchHumidityData(timeRange) {
    try {
        const response = await fetch(`/humidity/${timeRange}`);
        if (!response.ok) throw new Error("Failed to fetch humidity data");
        const data = await response.json();

        // Extract timestamps and humidity values
        let labels = data.map(entry => entry.timestamp);
        const humidityLevels = data.map(entry => entry.humidity);

        // Convert numeric indices to time labels if needed
        if (labels.length > 0 && typeof labels[0] === 'number') {
            // If timestamps are just numeric indices, create time-based labels
            const now = new Date();
            const minutes = timeRange.includes('min') ? parseInt(timeRange) : 60;
            const interval = minutes / labels.length;

            // Create time labels working backward from now
            labels = labels.map((_, index) => {
                const time = new Date(now.getTime() - (labels.length - 1 - index) * interval * 60000);
                return time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            });
        }

        // Update the humidity chart
        updateHumidityChart(labels, humidityLevels);
    } catch (error) {
        console.error("Error fetching humidity data:", error);
    }
}

function updateHumidityChart(labels, humidityLevels) {
    if (window.humidityChart) {
        window.humidityChart.data.labels = labels;
        window.humidityChart.data.datasets[0].data = humidityLevels;
        window.humidityChart.update();
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////
function setupLightChart() {
    const ctx = document.getElementById('lightChart');
    if (!ctx) return;

    window.lightChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Outside Light',
                    data: [],
                    borderColor: 'rgba(241, 196, 15, 1)',  // Yellow for outside light
                    backgroundColor: 'rgba(241, 196, 15, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointStyle: false,
                },
                {
                    label: 'Inside Light',
                    data: [],
                    borderColor: 'rgba(243, 156, 18, 1)',  // Orange for inside light
                    backgroundColor: 'rgba(243, 156, 18, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointStyle: false,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        boxWidth: 12,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const datasetLabel = context.dataset.label || '';
                            return `${datasetLabel}: ${context.parsed.y} lux`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        callback: function (value) {
                            return value + ' lux';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Light Level (lux)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 5,
                        callback: function(value, index, ticks) {
                            // If labels are already formatted as time strings, use them directly
                            time = window.lightChart.data.labels[index];
                            // If time is in 12-hour format (like "2:30 PM"), convert to 24-hour format
                            if (time && time.includes(':')) {
                                // Check if it's already in the format we need
                                if (time.includes(' ')) {
                                    const [timePart, meridiem] = time.split(' ');
                                    const [hour, minute] = timePart.split(':').map(Number);
                                    
                                    // Convert to 24-hour format
                                    let hour24 = hour;
                                    if (meridiem === 'PM' && hour < 12) hour24 += 12;
                                    if (meridiem === 'AM' && hour === 12) hour24 = 0;
                                    
                                    time = `${hour24.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
                                }
                            }
                            return time || value;
                        }
                    }
                }
            }
        }
    });
}

async function fetchLightData(timeRange) {
    try {
        const response = await fetch(`/light/${timeRange}`);
        if (!response.ok) throw new Error("Failed to fetch light data");
        const data = await response.json();

        // Extract timestamps and light values
        let labels = data.map(entry => entry.timestamp);
        const outsideLevels = data.map(entry => entry.outside_light);
        const insideLevels = data.map(entry => entry.inside_light);

        // Convert numeric indices to time labels if needed
        if (labels.length > 0 && typeof labels[0] === 'number') {
            // If timestamps are just numeric indices, create time-based labels
            const now = new Date();
            const minutes = timeRange.includes('min') ? parseInt(timeRange) : 60;
            const interval = minutes / labels.length;

            // Create time labels working backward from now
            labels = labels.map((_, index) => {
                const time = new Date(now.getTime() - (labels.length - 1 - index) * interval * 60000);
                return time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            });
        }

        // Update the light chart
        updateLightChart(labels, outsideLevels, insideLevels);
    } catch (error) {
        console.error("Error fetching light data:", error);
    }
}

function updateLightChart(labels, outsideLevels, insideLevels) {
    if (window.lightChart) {
        window.lightChart.data.labels = labels;
        window.lightChart.data.datasets[0].data = outsideLevels;
        window.lightChart.data.datasets[1].data = insideLevels;
        window.lightChart.update();
    }
}
////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////


