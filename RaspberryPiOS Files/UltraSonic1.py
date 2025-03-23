import RPi.GPIO as GPIO
import time

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
    # Ensure the trigger pin is low
    GPIO.output(TRIG, False)
    time.sleep(2)  # Allow sensor to settle

    # Trigger the sensor by setting it high for 10 microseconds
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Measure the time between sending and receiving the signal
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    # Calculate distance
    distance = pulse_duration * 17150  # Speed of sound at sea level is ~34300 cm/s, divided by 2

    distance = round(distance, 2)  # Round to two decimal places
    return distance

try:
    while True:
        dist = measure_distance()
        print("Distance:", dist, "cm")
        time.sleep(1)  # Wait for 1 second before the next measurement

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
