import RPi.GPIO as GPIO
import time
import json
import requests
from datetime import datetime

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
TRIG = 23
ECHO = 24

# Set up the GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function to measure distance
def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(2)  # Allow sensor to settle

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    timeout = time.time() + 1
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if time.time() > timeout:
            return None

    pulse_end = time.time()
    timeout = time.time() + 1
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if time.time() > timeout:
            return None

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

# Function to calculate the percentage based on distance
def calculate_percentage(distance, max_distance=65):
    if distance > max_distance:
        percentage = (distance / max_distance) * 100
    else:
        percentage = (distance / max_distance) * 100
    return round(percentage, 2)

# Function to save data to a JSON file
def save_to_json(data):
    filename = f"Ultrasonic_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")

# Function to send the percentage data to the API
def post_percentage_to_api(percentage):
    url = "https://localhost:44346/odata/WaterLevelOData"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # Include this if your API requires authentication
    }
    data = {
        "_id": "66c89e1e094adef638f5558d",  # Replace with the actual ID if it changes
        "TankId": "6",
        "WaterPushedOn": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "Percentage": percentage,
        "RaspberrypiId": "raspi15"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:  # Assuming 201 Created is the success status code
        print("Percentage data posted successfully")
    else:
        print(f"Failed to post percentage data. Status code: {response.status_code}")
        print(response.text)

try:
    last_save_time = time.time()
    while True:
        dist = measure_distance()
        if dist is not None:
            percentage = calculate_percentage(dist)
            print(f"Distance: {dist} cm, Percentage: {percentage}%")
            
            # Check if 2 minutes have passed since the last save
            current_time = time.time()
            if current_time - last_save_time >= 120:  # 120 seconds = 2 minutes
                # Prepare data for JSON file
                data = {
                    "Distance (cm)": dist,
                    "Percentage (%)": percentage,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_to_json(data)
                post_percentage_to_api(percentage)  # Post data to API
                last_save_time = current_time  # Update the last save time
            
        else:
            print("Measurement failed")
        time.sleep(20)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
