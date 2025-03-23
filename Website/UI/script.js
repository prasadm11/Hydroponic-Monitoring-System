const phLevel = 7.5; 
const phNeedle = document.getElementById('ph-needle');


const phAngle = ((phLevel / 14) * 180) - 90; 

phNeedle.style.transform = `rotate(${phAngle}deg)`;


document.getElementById('ph-level').innerText = phLevel;

document.getElementById("water-pump-start").addEventListener("click", function() {
    console.log("Start button for water pump clicked");
    fetch('https://hydroponic.cloud/turn_on/25', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.ok) {
            document.getElementById("water-pump-state").textContent = "On";
            console.log("Water pump motor started successfully");
        } else {
            console.error("Error starting water pump.");
        }
    })
    .catch(error => {
        console.error("Error starting water pump:", error);
    });
});


document.getElementById("water-pump-stop").addEventListener("click", function() {
    console.log("Stop button for water pump clicked");
    fetch('https://hydroponic.cloud/turn_off/25', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.ok) {
            document.getElementById("water-pump-state").textContent = "Off";
            console.log("Water pump motor stopped successfully");
        } else {
            console.error("Error stopping water pump.");
        }
    })
    .catch(error => {
        console.error("Error stopping water pump:", error);
    });
});


document.getElementById("fertilizer-pump-start").addEventListener("click", function() {
    console.log("Start button for fertilizer pump clicked");
    fetch('https://hydroponic.cloud/turn_on/26', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.ok) {
            document.getElementById("fertilizer-pump-state").textContent = "On";
            console.log("Fertilizer pump motor started successfully");
        } else {
            console.error("Error starting fertilizer pump.");
        }
    })
    .catch(error => {
        console.error("Error starting fertilizer pump:", error);
    });
});


document.getElementById("fertilizer-pump-stop").addEventListener("click", function() {
    console.log("Stop button for fertilizer pump clicked");
    fetch('https://hydroponic.cloud/turn_off/26', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.ok) {
            document.getElementById("fertilizer-pump-state").textContent = "Off";
            console.log("Fertilizer pump motor stopped successfully");
        } else {
            console.error("Error stopping fertilizer pump.");
        }
    })
    .catch(error => {
        console.error("Error stopping fertilizer pump:", error);
    });
});



function addAlert(message) {
    const alertsList = document.getElementById('alerts-list');
    const alertItem = document.createElement('li');
    alertItem.textContent = message;
    alertsList.appendChild(alertItem);
}

function startVideo() {
    const videoSource = "https://hydroponic.cloud/video_feed";
    const cameraFeed = document.getElementById("camera-feed");
    
    cameraFeed.src = videoSource;
    cameraFeed.style.display = "block"; 

    document.getElementById("start-button").disabled = true;
    document.getElementById("stop-button").disabled = false;
}

function stopVideo() {
    const cameraFeed = document.getElementById("camera-feed");
    
    cameraFeed.src = "";  
    cameraFeed.style.display = "none"; 

    document.getElementById("start-button").disabled = false;
    document.getElementById("stop-button").disabled = true;
}


document.addEventListener("DOMContentLoaded", function() {
    stopVideo(); 
});



function fetchWaterLevel() {
    fetch('https://hydroponic.cloud/distance', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); 
    })
    .then(data => {
        
        const waterPercentage = data.percentage; 

        document.getElementById("water-level").textContent = `${waterPercentage}%`;

        let tankStatus = "Full";
        if (waterPercentage < 30) {
            tankStatus = "Low";
        } else if (waterPercentage < 70) {
            tankStatus = "Medium";
        }
        document.getElementById("tank-status").textContent = tankStatus;

        const tankElement = document.getElementById("water-tank");
        tankElement.style.height = waterPercentage + '%'; 
        tankElement.style.backgroundColor = '#007bff'; 
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}
fetchWaterLevel();


setInterval(fetchWaterLevel, 10000);

function fetchTemperature() {
    fetch('https://api.open-meteo.com/v1/forecast?latitude=18.735&longitude=73.6756&current=temperature_2m,relative_humidity_2m')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch temperature: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Temperature Data:', data);
            const temperature = data.current.temperature_2m;
            document.getElementById("temperature").textContent = `${temperature}°C`;
        })
        .catch(error => {
            console.error('Error fetching temperature:', error);
            document.getElementById("temperature").textContent = 'Error';
        });
}

function fetchHumidity() {
    fetch('https://api.open-meteo.com/v1/forecast?latitude=18.735&longitude=73.6756&current=temperature_2m,relative_humidity_2m')
        .then(response => {
            if (!response.ok) {
                console.error('HTTP error', response.status, response.statusText);
                throw new Error('Failed to fetch humidity: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Humidity Data:', data);
            
            const humidity = data.current.relative_humidity_2m; 
            console.log('Humidity Value:', humidity);

            if (humidity !== undefined && humidity !== null) {
                document.getElementById("humidity").textContent = `${humidity}%`;
            } else {
                document.getElementById("humidity").textContent = 'N/A';
            }
        })
        .catch(error => {
            console.error('Error fetching humidity:', error);
            document.getElementById("humidity").textContent = 'Error';
        });
}

fetchTemperature();
fetchHumidity();
setInterval(fetchTemperature, 10000);
setInterval(fetchHumidity, 10000);


const autoWaterCheckbox = document.getElementById('auto-water-checkbox');
const autoFertilizerCheckbox = document.getElementById('auto-fertilizer-checkbox');
const autoWaterStatus = document.getElementById('auto-water-status');
const autoFertilizerStatus = document.getElementById('auto-fertilizer-status');


autoWaterCheckbox.addEventListener('change', function() {
    if (autoWaterCheckbox.checked) {
        autoWaterStatus.textContent = 'Enabled';
        autoWaterStatus.style.color = 'green';
    } else {
        autoWaterStatus.textContent = 'Disabled';
        autoWaterStatus.style.color = 'red';
    }
});


autoFertilizerCheckbox.addEventListener('change', function() {
    if (autoFertilizerCheckbox.checked) {
        autoFertilizerStatus.textContent = 'Enabled';
        autoFertilizerStatus.style.color = 'green';
    } else {
        autoFertilizerStatus.textContent = 'Disabled';
        autoFertilizerStatus.style.color = 'red';
    }
});


document.addEventListener('DOMContentLoaded', function() {
    let waterPumpInterval, fertilizerPumpInterval;
    const waterLevelThreshold = 30; 


    function checkWaterLevel() {
        fetch('https://hydroponic.cloud/distance') 
            .then(response => response.json())
            .then(data => {
                const waterLevel = data.percentage; 
                console.log(`Current water level: ${waterLevel}%`);

                if (waterLevel < waterLevelThreshold) {
                    console.log("Water level is below threshold. Turning off water pump and disabling auto mode.");
                    document.getElementById('auto-water-checkbox').checked = false;
                    autoWaterPumpControl(); 
                    document.getElementById("water-pump-stop").click(); 
                }
            })
            .catch(error => {
                console.error("Error fetching water level:", error);
            });
    }

    function autoWaterPumpControl() {
        const autoWaterCheckbox = document.getElementById('auto-water-checkbox');
        const waterPumpStatus = document.getElementById('auto-water-status');

        if (autoWaterCheckbox.checked) {
            waterPumpStatus.textContent = "Enabled";

            waterLevelCheckInterval = setInterval(checkWaterLevel, 10000); 

            console.log("Auto mode: Starting Water Pump immediately");
            document.getElementById("water-pump-start").click(); 

            setTimeout(() => {
                console.log("Auto mode: Stopping Water Pump");
                document.getElementById("water-pump-stop").click(); 
            }, 900000);

            waterPumpInterval = setInterval(() => {
                console.log("Auto mode: Starting Water Pump (interval)");
                document.getElementById("water-pump-start").click(); 

                setTimeout(() => {
                    console.log("Auto mode: Stopping Water Pump (interval)");
                    document.getElementById("water-pump-stop").click(); 
                }, 900000);
            }, 2100000); 

        } else {
            clearInterval(waterPumpInterval); 
            clearInterval(waterLevelCheckInterval);  
            waterPumpStatus.textContent = "Disabled";
            document.getElementById("water-pump-stop").click(); 
        }
    }

    function autoFertilizerPumpControl() {
        const autoFertilizerCheckbox = document.getElementById('auto-fertilizer-checkbox');
        const fertilizerPumpStatus = document.getElementById('auto-fertilizer-status');

        if (autoFertilizerCheckbox.checked) {
            fertilizerPumpStatus.textContent = "Enabled";

            console.log("Auto mode: Starting Fertilizer Pump immediately");
            document.getElementById("fertilizer-pump-start").click();  

            setTimeout(() => {
                console.log("Auto mode: Stopping Fertilizer Pump");
                document.getElementById("fertilizer-pump-stop").click(); 
            }, 420000);

            fertilizerPumpInterval = setInterval(() => {
                console.log("Auto mode: Starting Fertilizer Pump (interval)");
                document.getElementById("fertilizer-pump-start").click();  

                setTimeout(() => {
                    console.log("Auto mode: Stopping Fertilizer Pump (interval)");
                    document.getElementById("fertilizer-pump-stop").click();  
                }, 420000);
            }, 25620000);  

        } else {
            clearInterval(fertilizerPumpInterval);  
            fertilizerPumpStatus.textContent = "Disabled";
            document.getElementById("fertilizer-pump-stop").click();  
        }
    }

    document.getElementById('auto-water-checkbox').addEventListener('change', autoWaterPumpControl);
    document.getElementById('auto-fertilizer-checkbox').addEventListener('change', autoFertilizerPumpControl);
});
