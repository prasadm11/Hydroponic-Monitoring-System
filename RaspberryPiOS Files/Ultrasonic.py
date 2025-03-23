from gpiozero import DistanceSensor
from time import sleep

# Define the trigger and echo pins
TRIG_PIN = 3  # Change as per your connection
ECHO_PIN = 27  # Change as per your connection

# Initialize the DistanceSensor
sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, max_distance=2)

try:
    while True:
        distance = sensor.distance * 100  # Convert to centimeters
        if distance > 500 or distance == 0:
            print("Out of Range")
        else:
            print(f"{distance:.2f} cm")
        sleep(0.5)

except KeyboardInterrupt:
    print("Measurement stopped by User")
