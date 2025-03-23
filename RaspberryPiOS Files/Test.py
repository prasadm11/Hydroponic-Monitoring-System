import tkinter as tk
from tkinter import ttk
import requests
import RPi.GPIO as GPIO
import time
import threading

class HydroponicUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydroponic Monitoring System")
        self.root.configure(background="#f0f0f0")  # Light gray background
        
        # GPIO setup for motors and ultrasonic sensor
        self.motor_pins = [25, 26, 27, 17]  # GPIO pins connected to the relays for motors
        self.TRIG = 23  # GPIO pin for TRIG
        self.ECHO = 24  # GPIO pin for ECHO
        
        GPIO.setmode(GPIO.BCM)
        for pin in self.motor_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)  # Start with motors off
        
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

        self.weather_url = "https://api.open-meteo.com/v1/forecast?latitude=18.735&longitude=73.6756&current=temperature_2m,relative_humidity_2m"

        self.auto_mode = tk.BooleanVar(value=False)  # Variable to store auto mode state
        self.auto_mode_active = False
        self.fetching_active = False
        

        # Create a style
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 14))
        style.configure("TButton", font=("Helvetica", 12), padding=5)
        style.configure("TCheckbutton", font=("Helvetica", 12))

        # Create frames
        self.motor_frame = ttk.LabelFrame(self.root, text="Motor Status", padding=(10, 5))
        self.motor_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ew")
        
        self.water_frame = ttk.LabelFrame(self.root, text="Water Level", padding=(10, 5))
        self.water_frame.grid(column=0, row=1, padx=10, pady=10, sticky="ew")
        
        self.ph_frame = ttk.LabelFrame(self.root, text="pH Value", padding=(10, 5))
        self.ph_frame.grid(column=0, row=2, padx=10, pady=10, sticky="ew")
        
        self.temp_frame = ttk.LabelFrame(self.root, text="Temperature", padding=(10, 5))
        self.temp_frame.grid(column=0, row=3, padx=10, pady=10, sticky="ew")
        
        self.humidity_frame = ttk.LabelFrame(self.root, text="Humidity", padding=(10, 5))
        self.humidity_frame.grid(column=0, row=4, padx=10, pady=10, sticky="ew")

        # Motor Status
        self.motor_status_labels = []
        self.motor_leds = []
        for i in range(4):
            label = ttk.Label(self.motor_frame, text=f"Motor {i+1} Status:")
            label.grid(column=0, row=i, sticky=tk.W, padx=10, pady=10)
            self.motor_status_labels.append(label)
            
            motor_led = tk.Canvas(self.motor_frame, width=20, height=20)
            motor_led.grid(column=1, row=i, padx=10, pady=10)
            self.motor_leds.append(motor_led)
            
            status_value = ttk.Label(self.motor_frame, text="OFF")
            status_value.grid(column=2, row=i, sticky=tk.W, padx=10, pady=10)
            self.motor_status_labels.append(status_value)

        # Water Level
        self.water_level_label = ttk.Label(self.water_frame, text="Level:")
        self.water_level_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        
        self.water_level_bar = ttk.Progressbar(self.water_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.water_level_bar.grid(column=1, row=0, sticky=tk.EW, padx=10, pady=10)
        
        self.water_level_value = ttk.Label(self.water_frame, text="0%")
        self.water_level_value.grid(column=2, row=0, sticky=tk.W, padx=10, pady=10)

        # pH Value
        self.ph_value_label = ttk.Label(self.ph_frame, text="Value:")
        self.ph_value_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        
        self.ph_value_display = ttk.Label(self.ph_frame, text="0.0")
        self.ph_value_display.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)
        
        # Temperature
        self.temperature_label = ttk.Label(self.temp_frame, text="Current:")
        self.temperature_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        
        self.temperature_display = ttk.Label(self.temp_frame, text="0.0 °C")
        self.temperature_display.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)

        # Humidity
        self.humidity_label = ttk.Label(self.humidity_frame, text="Current:")
        self.humidity_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        
        self.humidity_display = ttk.Label(self.humidity_frame, text="0.0%")
        self.humidity_display.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)

        # Control Buttons
        self.control_frame = ttk.LabelFrame(self.root, text="Motor Control", padding=(10, 5))
        self.control_frame.grid(column=0, row=5, padx=10, pady=10, sticky="ew")

        self.motor_control_buttons = []
        for i in range(4):
            start_button = ttk.Button(self.control_frame, text=f"Start Motor {i+1}", command=lambda i=i: self.start_motor(i))
            start_button.grid(column=0, row=i, padx=10, pady=10)
            stop_button = ttk.Button(self.control_frame, text=f"Stop Motor {i+1}", command=lambda i=i: self.stop_motor(i))
            stop_button.grid(column=1, row=i, padx=10, pady=10)
            self.motor_control_buttons.append((start_button, stop_button))
        
        # Auto Mode Toggle
        self.auto_mode_toggle = ttk.Checkbutton(self.control_frame, text="Auto Mode", variable=self.auto_mode, command=self.toggle_auto_mode)
        self.auto_mode_toggle.grid(column=2, row=0, padx=10, pady=10)

        # Start/Stop Fetching
        self.fetch_control_frame = ttk.LabelFrame(self.root, text="Data Fetching Control", padding=(10, 5))
        self.fetch_control_frame.grid(column=0, row=6, padx=10, pady=10, sticky="ew")

        self.start_fetching_button = ttk.Button(self.fetch_control_frame, text="Start Fetching", command=self.start_fetching)
        self.start_fetching_button.grid(column=0, row=0, padx=10, pady=10)

        self.stop_fetching_button = ttk.Button(self.fetch_control_frame, text="Stop Fetching", command=self.stop_fetching)
        self.stop_fetching_button.grid(column=1, row=0, padx=10, pady=10)

        # Log Area
        self.log_frame = ttk.LabelFrame(self.root, text="Logs", padding=(10, 5))
        self.log_frame.grid(column=0, row=7, padx=10, pady=10, sticky="nsew")

        self.log_text = tk.Text(self.log_frame, height=8, width=60, wrap=tk.WORD)
        self.log_text.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        # Set row/column weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(0, weight=1)
        self.log_frame.grid_columnconfigure(0, weight=1)

        # Start the update loop
        self.update_values()

    def fetch_data(self, url, label):
        try:
            self.log(f"Fetching data from {label}...")
            response = requests.get(url, verify=False)  # Disable SSL verification
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            self.log(f"Data fetched from {label}: {data}")
            return data
        except requests.RequestException as e:
            self.log(f"Error fetching data from {label}: {e}")
            return None

    def control_motor(self, motor_index, action):
        try:
            self.log(f"Sending '{action}' command to Motor {motor_index + 1}...")
            if action == "start":
                GPIO.output(self.motor_pins[motor_index], GPIO.LOW)  # Activate motor
                self.update_motor_status(motor_index, "ON")
            elif action == "stop":
                GPIO.output(self.motor_pins[motor_index], GPIO.HIGH)  # Deactivate motor
                self.update_motor_status(motor_index, "OFF")
        except Exception as e:
            self.log(f"Error controlling Motor {motor_index + 1}: {e}")

    def update_motor_status(self, motor_index, status):
        self.motor_status_labels[motor_index * 2 + 1].config(text=status)  # Update status label
        color = "green" if status == "ON" else "red"
        self.motor_leds[motor_index].create_oval(0, 0, 20, 20, fill=color)

    def start_motor(self, motor_index):
        self.control_motor(motor_index, "start")

    def stop_motor(self, motor_index):
        self.control_motor(motor_index, "stop")

    def toggle_auto_mode(self):
        if self.auto_mode.get():
            self.auto_mode_active = True
            self.log("Auto Mode activated.")
            threading.Thread(target=self.auto_mode_logic, daemon=True).start()
        else:
            self.auto_mode_active = False
            self.log("Auto Mode deactivated.")

    def auto_mode_logic(self):
        while self.auto_mode_active:
            for motor_index in range(4):
                self.start_motor(motor_index)
                time.sleep(15 * 60)  # On for 15 minutes
                self.stop_motor(motor_index)
                time.sleep(13 * 60)  # Off for 13 minutes

    def start_fetching(self):
        if not self.fetching_active:
            self.fetching_active = True
            self.log("Data fetching started.")
            self.update_weather()
            self.update_water_level()
            self.update_ph()
            self.update_temperature_humidity()
            self.fetching_thread = threading.Thread(target=self.fetch_loop, daemon=True)
            self.fetching_thread.start()

    def fetch_loop(self):
        while self.fetching_active:
            self.update_weather()
            self.update_water_level()
            self.update_ph()
            self.update_temperature_humidity()
            time.sleep(60)  # Fetch every minute

    def stop_fetching(self):
        self.fetching_active = False
        self.log("Data fetching stopped.")

    def update_weather(self):
        data = self.fetch_data(self.weather_url, "weather")
        if data:
            temperature = data.get("current_temperature_2m")
            humidity = data.get("relative_humidity_2m")
            if temperature is not None:
                self.temperature_display.config(text=f"{temperature:.1f} °C")
            if humidity is not None:
                self.humidity_display.config(text=f"{humidity:.1f}%")

    def update_water_level(self):
        # Simulated water level update (replace with actual sensor code)
        distance = self.get_distance()  # Replace this with actual distance measuring function
        percentage = self.calculate_percentage(distance)
        self.water_level_bar['value'] = percentage
        self.water_level_value.config(text=f"{percentage}%")
    
    def calculate_percentage(self, distance):
        max_distance = 65.0  # 100% corresponds to 65 cm
        if distance <= max_distance:
            return int((1 - distance / max_distance) * 100)
        else:
            return 0

    def update_ph(self):
        # Simulated pH value update (replace with actual sensor code)
        ph_value = 7.0  # Replace this with the actual pH reading
        self.ph_value_display.config(text=f"{ph_value:.1f}")

    def get_distance(self):
        GPIO.output(self.TRIG, GPIO.HIGH)
        time.sleep(0.00001)  # 10 microseconds
        GPIO.output(self.TRIG, GPIO.LOW)

        start_time = time.time()
        while GPIO.input(self.ECHO) == 0:
            start_time = time.time()
        
        stop_time = time.time()
        while GPIO.input(self.ECHO) == 1:
            stop_time = time.time()

        time_elapsed = stop_time - start_time
        distance = time_elapsed * 34300 / 2  # Speed of sound is 34300 cm/s
        return distance

    def update_temperature_humidity(self):
        # Simulated temperature and humidity update (replace with actual sensor code)
        temperature = 25.0  # Replace this with the actual temperature reading
        humidity = 50.0  # Replace this with the actual humidity reading

        self.temperature_display.config(text=f"{temperature:.1f} °C")
        self.humidity_display.config(text=f"{humidity:.1f}%")

    def update_values(self):
        # Update the values and schedule the next update
        self.update_water_level()
        self.update_ph()
        self.update_temperature_humidity()
        self.root.after(1000, self.update_values)  # Update every second

    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)  # Scroll to the end of the log

    def __del__(self):
        GPIO.cleanup()

if __name__ == "__main__":
    root = tk.Tk()
    app = HydroponicUI(root)
    root.mainloop()
