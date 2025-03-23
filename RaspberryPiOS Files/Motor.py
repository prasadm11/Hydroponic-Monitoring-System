import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) 

GPIO.setup(25, GPIO.OUT)  # output pin


print("Testing RF out, Press CTRL+C to exit")

try:
    while True:
        GPIO.output(25, GPIO.LOW)
        print("set GPIO LOW")
        time.sleep(12*60)     
        GPIO.output(25, GPIO.HIGH)
        print("set GPIO HIGH")
        time.sleep(15*60)
              
except KeyboardInterrupt:
    print("Keyboard interrupt")

except Exception as e:
    print(f"Some error: {e}") 

finally:
    print("Clean up") 
    GPIO.cleanup()  
