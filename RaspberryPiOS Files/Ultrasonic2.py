import RPi.GPIO as GPIO
import time
import json
import requests
from datetime import datetime
from pymongo import MongoClient, WriteConcern

# MongoDB connection setup
connection_string = "mongodb+srv://prasadmahajan6735:Prasad%405050@mongodbcrud.ugxblmb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client['MongoDBCRUD']  # Replace with your database name
collection = db.get_collection('WaterLevel', write_concern=WriteConcern("majority", wtimeout=1000))

# GPIO setup
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function to measure distance
def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(2)
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
    return round(distance, 2)

# Function to calculate percentage
def calculate_percentage(distance, max_distance=65):
    percentage = (distance / max_distance) * 100
    return round(percentage, 2)

# Function to save data to a JSON file
def save_to_json(data):
    filename = f"Ultrasonic_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")

# Function to read data from JSON file and push to MongoDB
def push_to_mongodb(data):
    # Extract the percentage value
    percentage = data["Percentage (%)"]
    # Create the document to update
    update_filter = {"RaspberrypiId": "raspicluster", "TankId": "T13"}
    update_data = {
        "$set": {
            "Percentage": percentage,
            "WaterPushedOn": datetime.utcnow()
        }
    }
    result = collection.update_one(update_filter, update_data)
    if result.matched_count > 0:
        print("Percentage updated successfully.")
    else:
        print("No matching document found.")

try:
    last_save_time = time.time()
    while True:
        dist = measure_distance()
        if dist is not None:
            percentage = calculate_percentage(dist)
            print(f"Distance: {dist} cm, Percentage: {percentage}%")
            
            # Prepare data for JSON file
            data = {
                "Distance (cm)": dist,
                "Percentage (%)": percentage,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_to_json(data)

            # Push data to MongoDB every 30 seconds
            current_time = time.time()
            if current_time - last_save_time >= 30:
                push_to_mongodb(data)
                last_save_time = current_time
            
        else:
            print("Measurement failed")
        time.sleep(20)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
