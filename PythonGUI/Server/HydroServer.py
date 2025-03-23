from flask import Flask, Response, request, render_template_string
import RPi.GPIO as GPIO
import time
import cv2
import atexit
import os
from threading import Lock

app = Flask(__name__)

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Relay pins
relay_pins = [25, 26, 27, 17]
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# Ultrasonic sensor pins
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Open the webcam (0 is typically the first camera)
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Use appropriate backend (V4L2 for Linux)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Set resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def cleanup():
    cap.release()
    if RPI_ENV:
        GPIO.cleanup()  # Cleanup GPIO on exit

atexit.register(cleanup)


speak_count = 0
speak_count_lock = Lock()
@app.route('/speak_warning', methods=['GET'])
def speak_warning():
    global speak_count
    with speak_count_lock:
        if speak_count >= 3:
            return "Warning already spoken 3 times", 200  # Don't speak if already 3 times
        
        # Use espeak to speak the warning message
        message = "Water level is below 30 percent, please fill immediately."
        os.system(f'espeak "{message}"')

        # Increment the speak count
        speak_count += 1

def calculate_percentage(distance, max_distance=61.7):
    try:
        if distance is not None and distance > 0:
            percentage = (distance / max_distance) * 100
            return 100 - round(percentage, 2)  # Full is 0%, empty is 100%
        return None
    except Exception as e:
        print(f"Error calculating percentage: {e}")
        return None

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/video_feed')
def video_feed():
    def generate_frames():
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Prevent lag
        while True:
            success, frame = cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    break
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(0.05)  # Adjust for frame rate

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def home():
    # HTML template with a welcome message
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hydroponics Server</title>
    </head>
    <body>
        <h4>Welcome to Hydroponics Server</h4>
        <p>Use the following endpoints:</p>
        <ul>
            <li><strong>/turn_on/&lt;pin&gt;</strong> - Turn on relay pin</li>
            <li><strong>/turn_off/&lt;pin&gt;</strong> - Turn off relay pin</li>
            <li><strong>/status</strong> - Get relay status</li>
            <li><strong>/distance</strong> - Get distance from ultrasonic sensor</li>
            <li><strong>/video_feed</strong> - Get live video feed</li>
        </ul>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/turn_on/<int:pin>', methods=['POST'])
def turn_on(pin):
    if pin in relay_pins:
        GPIO.output(pin, GPIO.LOW)
        return f"Turned On pin {pin}", 200
    return "Invalid pin", 400

@app.route('/turn_off/<int:pin>', methods=['POST'])
def turn_off(pin):
    if pin in relay_pins:
        GPIO.output(pin, GPIO.HIGH)
        return f"Turned Off pin {pin}", 200
    return "Invalid pin", 400

@app.route('/status', methods=['GET'])
def status():
    status = {pin: GPIO.input(pin) for pin in relay_pins}
    return status, 200

@app.route('/distance', methods=['GET'])
def distance():
    # Trigger the ultrasonic sensor
    GPIO.output(TRIG, True)
    time.sleep(0.01)
    GPIO.output(TRIG, False)

    # Measure the duration of the echo
    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    # Calculate the distance
    elapsed_time = stop_time - start_time
    distance_cm = (elapsed_time * 34300) / 2  # Speed of sound is 34300 cm/s

    # Calculate percentage
    percentage = calculate_percentage(distance_cm)

    return {'distance': distance_cm, 'percentage': percentage}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
