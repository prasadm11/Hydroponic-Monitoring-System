import tkinter as tk
from tkinter import ttk, messagebox
import requests

class HydroponicUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydroponic Monitoring System")
        self.root.configure(background="#f0f0f0")  # Light gray background
        
        # URLs for APIs
        self.motor_status_url = "https://localhost:7274/odata/MotorStatusOData?$orderby=Id desc &$top=1"
        self.water_level_url = "https://localhost:7274/odata/WaterLevelOData?$orderby=Id desc &$top=1"
        self.ph_value_url = "https://localhost:7274/odata/PhInfoOData?$orderby=Id desc &$top=1"
        self.control_motor_url = "https://localhost:7274/odata/ControlMotorOData"
        self.weather_url = "https://api.open-meteo.com/v1/forecast?latitude=18.735&longitude=73.6756&current=temperature_2m,relative_humidity_2m"

        self.auto_mode = tk.BooleanVar(value=True)  # Variable to store auto mode state
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
        self.motor_status_label = ttk.Label(self.motor_frame, text="Status:")
        self.motor_status_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        
        self.motor_led = tk.Canvas(self.motor_frame, width=20, height=20)
        self.motor_led.grid(column=1, row=0, padx=10, pady=10)
        
        self.motor_status_value = ttk.Label(self.motor_frame, text="OFF")
        self.motor_status_value.grid(column=2, row=0, sticky=tk.W, padx=10, pady=10)
        
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

        self.start_motor_button = ttk.Button(self.control_frame, text="Start Motor", command=self.start_motor)
        self.start_motor_button.grid(column=0, row=0, padx=10, pady=10)

        self.stop_motor_button = ttk.Button(self.control_frame, text="Stop Motor", command=self.stop_motor)
        self.stop_motor_button.grid(column=1, row=0, padx=10, pady=10)
        
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

    def control_motor(self, action):
        try:
            self.log(f"Sending '{action}' command to motor...")
            response = requests.post(self.control_motor_url, json={"action": action}, verify=False)  # Disable SSL verification
            response.raise_for_status()  # Raise an exception for HTTP errors
            self.log(f"Motor {action} command sent successfully.")
        except requests.RequestException as e:
            self.log(f"Error controlling motor: {e}")

    def start_motor(self):
        if not self.auto_mode.get():
            self.log("Starting motor...")
            self.control_motor("start")

    def stop_motor(self):
        if not self.auto_mode.get():
            self.log("Stopping motor...")
            self.control_motor("stop")

    def toggle_auto_mode(self):
        if self.auto_mode.get():
            self.log("Auto mode enabled.")
            self.start_motor_button.state(['disabled'])
            self.stop_motor_button.state(['disabled'])
        else:
            self.log("Auto mode disabled.")
            self.start_motor_button.state(['!disabled'])
            self.stop_motor_button.state(['!disabled'])

    def start_fetching(self):
        if not self.fetching_active:
            self.fetching_active = True
            self.log("Started fetching data.")
            self.update_values()

    def stop_fetching(self):
        self.fetching_active = False
        self.log("Stopped fetching data.")

    def update_values(self):
        if self.fetching_active:
            # Fetch and update motor status
            motor_data = self.fetch_data(self.motor_status_url, "Motor Status")
            if motor_data:
                latest_motor_status = motor_data['value'][0] if motor_data['value'] else None
                if latest_motor_status:
                    motor_status = latest_motor_status['motorStatus']
                    self.motor_status_value.config(text=motor_status)
                    self.motor_led.config(bg="green" if motor_status.lower() == "on" else "red")

            # Fetch and update water level
            water_data = self.fetch_data(self.water_level_url, "Water Level")
            if water_data:
                latest_water_level = water_data['value'][0] if water_data['value'] else None
                if latest_water_level:
                    water_level = latest_water_level['waterLevel']
                    self.water_level_bar['value'] = water_level
                    self.water_level_value.config(text=f"{water_level}%")

            # Fetch and update pH value
            ph_data = self.fetch_data(self.ph_value_url, "pH Value")
            if ph_data:
                latest_ph_value = ph_data['value'][0] if ph_data['value'] else None
                if latest_ph_value:
                    ph_value = latest_ph_value['phValue']
                    self.ph_value_display.config(text=f"{ph_value:.1f}")

            # Fetch and update temperature and humidity
            weather_data = self.fetch_data(self.weather_url, "Weather API")
            if weather_data:
                temperature = weather_data.get('current_temperature', {}).get('temperature_2m')
                humidity = weather_data.get('current_humidity', {}).get('relative_humidity_2m')
                if temperature:
                    self.temperature_display.config(text=f"{temperature:.1f} °C")
                if humidity:
                    self.humidity_display.config(text=f"{humidity:.1f}%")

            self.root.after(5000, self.update_values)  # Update every 5 seconds

    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = HydroponicUI(root)
    root.mainloop()
