import RPi.GPIO as GPIO
import time

# GPIO pin connected to the Do pin of the pH sensor
PH_SENSOR_PIN = 17  # Change this to the GPIO pin you are using

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(PH_SENSOR_PIN, GPIO.IN)

def read_pH_sensor():
    # Read the value from the digital pin
    signal = GPIO.input(PH_SENSOR_PIN)
    print(f"Raw sensor value: {signal}")
    if signal:
        return "pH sensor signal HIGH"
    else:
        return "pH sensor signal LOW"

try:
    while True:
        # Read and print the sensor value
        pH_value = read_pH_sensor()
        print(f"pH Sensor Status: {pH_value}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup()
