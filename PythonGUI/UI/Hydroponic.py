# self.gif_image = Image.open("D:\HydroponicWorks\watering.gif")  # Replace with your GIF file path

import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import threading
import requests
import cv2  # Import OpenCV
from PIL import Image, ImageTk
import pyttsx3
from io import BytesIO




class HydroponicUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydroponic Monitoring System")
        #self.root.configure(background="#f0f0f0")  # Light gray background
        
        self.camera_running = False        
        self.fetching_active = False
        self.cap = None

        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  
        
        # Add canvas and scrollbar
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure canvas
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")

        self.video_source = "https://hydroponic.cloud/video_feed"
        gif_url = "https://hydroponic.cloud/static/watering.gif" 
        self.weather_url = "https://api.open-meteo.com/v1/forecast?latitude=18.735&longitude=73.6756&current=temperature_2m,relative_humidity_2m"
        self.percentage_url = "https://hydroponic.cloud/distance"
        self.speak_alert = "https://hydroponic.cloud/speak_warning"  # Replace with your actual Cloudflare Tunnel URL
        self.speak_count = 0  # Initialize the count for speaking warnings

        self.auto_mode_active = [False] * 4  # Auto mode state for each motor
        self.motor_states = [False] * 4  # Track motor states (True for ON, False for OFF)
        
        # Create a style
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 14))
        style.configure("TButton", font=("Helvetica", 12), padding=5)
        style.configure("TCheckbutton", font=("Helvetica", 12))

        # Create frames inside scrollable_frame
        self.motor_frame = ttk.LabelFrame(self.scrollable_frame, text="Motor Status", padding=(10, 10))
        self.motor_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ew", columnspan=2, ipadx=10, ipady=10)

        self.water_frame = ttk.LabelFrame(self.scrollable_frame, text="Water Level", padding=(10, 10))
        self.water_frame.grid(column=0, row=1, padx=10, pady=10, sticky="ew", ipadx=10, ipady=10)

        self.ph_frame = ttk.LabelFrame(self.scrollable_frame, text="pH Value", padding=(10, 10))
        self.ph_frame.grid(column=1, row=1, padx=10, pady=10, sticky="ew", ipadx=10, ipady=10)

        self.temp_frame = ttk.LabelFrame(self.scrollable_frame, text="Temperature", padding=(10, 10))
        self.temp_frame.grid(column=0, row=2, padx=10, pady=10, sticky="ew", ipadx=10, ipady=10)

        self.humidity_frame = ttk.LabelFrame(self.scrollable_frame, text="Humidity", padding=(10, 10))
        self.humidity_frame.grid(column=1, row=2, padx=10, pady=10, sticky="ew", ipadx=10, ipady=10)

        # Motor Status for 4 motors in a single row
        self.motor_status_labels = []
        self.motor_status_leds = []
        self.motor_status_values = []

        for i in range(4):
                motor_label = ttk.Label(self.motor_frame, text=f"Motor {i+1} :")
                motor_label.grid(column=i * 3, row=0, sticky=tk.W, padx=10, pady=(20, 20))
                self.motor_status_labels.append(motor_label)

                motor_led = tk.Canvas(self.motor_frame, width=20, height=20)
                motor_led.grid(column=i * 3 + 1, row=0, padx=20, pady=(20, 20))
                self.motor_status_leds.append(motor_led)

                motor_status_value = ttk.Label(self.motor_frame, text="OFF")
                motor_status_value.grid(column=i * 3 + 2, row=0, sticky=tk.W, padx=10, pady=(20, 20))
                self.motor_status_values.append(motor_status_value)
                
                # Initialize LED color based on the motor's status
                color = "red" if self.motor_states[i] is False else "green"
                motor_led.create_oval(2, 2, 20, 20, fill=color)  # Set the initial LED color

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
        
        self.temperature_display = ttk.Label(self.temp_frame, text="0.0 \u00B0C")
        self.temperature_display.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)

        # Humidity
        self.humidity_label = ttk.Label(self.humidity_frame, text="Current:")
        self.humidity_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        
        self.humidity_display = ttk.Label(self.humidity_frame, text="0.0%")
        self.humidity_display.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)

        # Control Buttons for Motors
        self.control_frame = ttk.LabelFrame(self.scrollable_frame, text="Motor Control", padding=(10, 10))
        self.control_frame.grid(column=0, row=4, padx=10, pady=10, sticky="ew", columnspan=2, ipadx=10, ipady=10)

        self.motor_buttons = []
        for i in range(4):
            motor_button = ttk.Button(self.control_frame, text=f"Start Motor {i+1}", command=lambda i=i: self.toggle_motor(i))
            motor_button.grid(column=i * 2, row=0, padx=10, pady=10)
            self.motor_buttons.append(motor_button)

            auto_checkbutton = ttk.Checkbutton(self.control_frame, text="Auto Mode", command=lambda i=i: self.toggle_auto_mode(i))
            auto_checkbutton.grid(column=i * 2 + 1, row=0, padx=10, pady=10)  # Removed the misplaced comma

        # Vision Monitoring Frame (added below Motor Control)
        self.vision_frame = ttk.LabelFrame(self.scrollable_frame, text="Vision Monitoring", padding=(10, 10))
        self.vision_frame.grid(column=0, row=5, padx=10, pady=10, sticky="ew", columnspan=2)

        # Subframe for camera view
        self.camera_view_frame = ttk.Frame(self.vision_frame, padding=(5, 5))
        self.camera_view_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        # Add camera preview label within the camera view frame
        self.camera_preview_label = ttk.Label(self.camera_view_frame, text="Camera Preview:")
        self.camera_preview_label.grid(column=0, row=0, padx=10, pady=10)

        # Canvas for displaying the camera feed
        self.camera_preview = tk.Canvas(self.camera_view_frame, width=800, height=400, bg="gray")        
        self.camera_preview.grid(column=0, row=1, padx=10, pady=10,sticky='nsew')
        
        # New: Define the vision_canvas for updating frames
        self.vision_canvas = tk.Canvas(self.camera_view_frame, width=800, height=400, bg="gray")
        self.vision_canvas.grid(column=0, row=1, padx=10, pady=10)
        
        # Create an extra frame for camera controls on the right side
        self.camera_control_frame = ttk.Frame(self.vision_frame,borderwidth=2, relief="solid")
        self.camera_control_frame.grid(column=1, row=0, padx=100, pady=200, sticky="ns")  # Align it next to the camera view

        # Add Start and Stop Camera buttons
        self.start_camera_button = ttk.Button(self.camera_control_frame, text="Start Camera", command=self.start_camera)
        self.start_camera_button.grid(column=3, row=1, padx=10, pady=10)  # Add button to grid

        self.stop_camera_button = ttk.Button(self.camera_control_frame, text="Stop Camera", command=self.stop_camera)
        self.stop_camera_button.grid(column=3, row=2, padx=10, pady=10)  # Add button to grid below

        
        # Load GIF 
        try:
            # Fetch the GIF from the server URL
            response = requests.get("https://hydroponic.cloud/static/watering.gif")
            response.raise_for_status()  # Check for request errors

            # Load the GIF from the response content
            self.gif_image = Image.open(BytesIO(response.content))
            self.gif_image_tk = ImageTk.PhotoImage(self.gif_image)
    
        except Exception as e:
            print(f"Error loading the GIF: {e}")
        
        
        self.frames = []  
        # Generate frames for GIF
        try:
                for i in range(self.gif_image.n_frames):
                        self.gif_image.seek(i)  # Move to the ith frame
                        frame = ImageTk.PhotoImage(self.gif_image.copy())
                        self.frames.append(frame)
        except Exception as e:
                print(f"Error loading GIF frames: {e}")

        self.current_frame = 0
        self.image_id = self.vision_canvas.create_image(400, 200, image=self.frames[self.current_frame])  # Center the GIF in the canvas

        # Store a reference to the frames
        self.frame_refs = self.frames  # Keep references to prevent garbage collection
        

        #Center the buttons in the frame
        self.camera_control_frame.columnconfigure(0, weight=1)  # Make the first column expand

        # Data Fetching Control Section
        self.data_fetch_frame = ttk.LabelFrame(self.scrollable_frame, text="Data Fetching Control", padding=(10, 10))
        self.data_fetch_frame.grid(column=0, row=6, padx=10, pady=10, sticky="ew", columnspan=2)

        self.start_fetching_button = ttk.Button(self.data_fetch_frame, text="Start Fetching", command=self.start_fetching)
        self.start_fetching_button.grid(column=0, row=0, padx=10, pady=10)

        self.stop_fetching_button = ttk.Button(self.data_fetch_frame, text="Stop Fetching", command=self.stop_fetching)
        self.stop_fetching_button.grid(column=1, row=0, padx=10, pady=10)

        # Log Frame
        self.log_frame = ttk.LabelFrame(self.scrollable_frame, text="Logs", padding=(10, 10))
        self.log_frame.grid(column=0, row=7, padx=10, pady=10, sticky="ew", columnspan=2)

        self.log_text_area = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, height=10, width=150)
        self.log_text_area.grid(column=0, row=0, padx=10, pady=10)

        # Start the data fetching in a separate thread
        self.fetch_thread = threading.Thread(target=self.fetch_data)
        self.fetch_thread.start()
        

        self.root.mainloop()

    # Function to toggle motor on/off
    # Function to toggle motor state
    def toggle_motor(self, motor_index):
        if self.motor_states[motor_index]:  # If motor is currently on, turn it off
            self.turn_off_motor(motor_index)
        else:  # If motor is off, turn it on
            self.turn_on_motor(motor_index)

        self.update_motor_status(motor_index)

    def update_motor_status(self, motor_index):
        """Update the motor status LED and label."""
        color = "green" if self.motor_states[motor_index] else "red"
        self.motor_status_leds[motor_index].delete("all")
        self.motor_status_leds[motor_index].create_oval(2, 2, 20, 20, fill=color)
        self.motor_status_values[motor_index]['text'] = "ON" if self.motor_states[motor_index] else "OFF"

    def turn_on_motor(self, motor_index):
        motor_pin = [25, 26, 27, 17][motor_index]  # GPIO pins for motors
        try:
            response = requests.post(f"https://hydroponic.cloud/turn_on/{motor_pin}")
            if response.status_code == 200:
                self.motor_states[motor_index] = True
                self.motor_buttons[motor_index].config(text=f"Stop Motor {motor_index + 1}")
                self.log_message(f"Motor {motor_index + 1} turned ON")
            else:
                self.log_message(f"Error turning on motor {motor_pin}: {response.status_code}")
        except Exception as e:
            self.log_message(f"Error: {e}")

    # Function to turn off motor
    def turn_off_motor(self, motor_index):
        motor_pin = [25, 26, 27, 17][motor_index]  # GPIO pins for motors
        try:
            response = requests.post(f"https://hydroponic.cloud/turn_off/{motor_pin}")
            if response.status_code == 200:
                self.motor_states[motor_index] = False
                self.motor_buttons[motor_index].config(text=f"Start Motor {motor_index + 1}")
                self.log_message(f"Motor {motor_index + 1} turned OFF")
            else:
                self.log_message(f"Error turning off motor {motor_pin}: {response.status_code}")
        except Exception as e:
            self.log_message(f"Error: {e}")
    


    # Function to toggle auto mode for motor
    def toggle_auto_mode(self, motor_index):
        if not self.auto_mode_active[motor_index]:
            self.auto_mode_active[motor_index] = True
            self.log_message(f"Auto mode activated for Motor {motor_index + 1}")
            threading.Thread(target=self.auto_mode_control, args=(motor_index,)).start()  # Start auto mode in a separate thread
        else:
            self.auto_mode_active[motor_index] = False
            self.log_message(f"Auto mode deactivated for Motor {motor_index + 1}")

    
    def auto_mode_control(self, motor_index):
        low_water_duration = 0  # Track how long water level is below 30%

        while self.auto_mode_active[motor_index]:
            try:
                # Fetch the current water level percentage
                response = requests.get(self.percentage_url)
                data = response.json()  # Assuming your server returns a JSON response
                water_level_percentage = data['percentage']  # Adjust this key based on your API response
                
                # Check the water level
                if motor_index == 0:  # For Motor 1, which checks the water level
                    if water_level_percentage < 30:
                        # Turn motor OFF if water level is below 30%
                        self.turn_off_motor(motor_index)
                        self.update_motor_status(motor_index)
                        self.log_message(f"Motor {motor_index + 1} turned OFF due to low water level.")
                        low_water_duration += 1  # Increment the duration counter

                        if low_water_duration == 15:  # If water level is below 30% for 15 seconds
                            try:
                                # Send a GET request to trigger the warning message
                                response = requests.get("https://hydroponic.cloud/speak_warning")
                
                                if response.status_code == 200:
                                    self.log_message("Successfully triggered the speech warning.")
                                else:
                                    self.log_message(f"Failed to trigger the speech warning. Status code: {response.status_code}")
                    
                            except Exception as e:
                                self.log_message(f"Error triggering the speech warning: {e}")


                        time.sleep(2)  # Wait for 2 second and continue checking the water level
                        continue  # Continue to check the water level
                    
                    else:
                        low_water_duration = 0  # Reset duration if water level is above 30%
                    
                    # Only proceed if water level is within the specified range (30% to 100%)
                    if 30 <= water_level_percentage <= 100:
                        self.turn_on_motor(motor_index)  # Turn motor ON
                        self.update_motor_status(motor_index)
                        
                        # Break 15 minutes (900 seconds) into 1-second intervals to check if auto mode is still active
                        for _ in range(900):
                                if not self.auto_mode_active[motor_index]:
                                        break  # Exit loop if auto mode is turned off
                                time.sleep(1)
                        
                        self.turn_off_motor(motor_index)  # Turn motor OFF
                        self.update_motor_status(motor_index)
                        
                        # Break 20 minutes (1200 seconds) into 1-second intervals to check if auto mode is still active
                        for _ in range(1200):
                                if not self.auto_mode_active[motor_index]:
                                        break  # Exit loop if auto mode is turned off
                                time.sleep(1)
                    
                    else:
                        # If the water level is not within the specified range, turn off the motor
                        self.turn_off_motor(motor_index)
                        self.update_motor_status(motor_index)
                        self.log_message(f"Motor {motor_index + 1} turned OFF due to water level out of range.")
                
                else:
                    # For Motor 2, 3, and 4 (assuming they are at indices 1, 2, and 3)
                    self.turn_on_motor(motor_index)  # Turn motor ON
                    self.update_motor_status(motor_index)
                    
                    # Break 7 minutes (420 seconds) into 1-second intervals
                    for _ in range(420):
                            if not self.auto_mode_active[motor_index]:
                                    break  # Exit loop if auto mode is turned off
                            time.sleep(1)
                    self.turn_off_motor(motor_index)  # Turn motor OFF
                    self.update_motor_status(motor_index)
                    
                    # Break 8 hours (28800 seconds) into 1-second intervals
                    for _ in range(28800):
                            if not self.auto_mode_active[motor_index]:
                                    break  # Exit loop if auto mode is turned off
                            time.sleep(1)

                time.sleep(1)  # Small delay before the next iteration to prevent busy waiting

            except Exception as e:
                print(f"Error in auto_mode_control: {e}")
                time.sleep(1)  # Sleep to avoid busy-waiting in case of an error

    
    def start_camera(self):
        if not self.camera_running:
            self.camera_running = True
            self.log_message("Camera started")
            self.video_stream = cv2.VideoCapture(self.video_source)
            self.update_camera()

    def stop_camera(self):
        if self.camera_running:
            self.camera_running = False
            self.log_message("Camera stopped")
            self.video_stream.release()
            self.vision_canvas.delete("all")  # Clear the canvas
            self.animate_gif() 

    def update_camera(self):
        if self.camera_running:
            ret, frame = self.video_stream.read()
            if ret:
                # Convert the image from BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert the image to PIL format
                img = Image.fromarray(frame)
                img = img.resize((800, 400), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                # Update the canvas with the new frame
                self.vision_canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.vision_canvas.image = img  # Keep a reference

            self.root.after(10, self.update_camera)


    def animate_gif(self):
            """Animate the GIF by cycling through frames."""
            if not self.camera_running and self.frames:
                    self.vision_canvas.delete("all")  # Clear the canvas before displaying the GIF
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    self.image_id = self.vision_canvas.create_image(400, 200, image=self.frames[self.current_frame])  # Center the GIF in the canvas
                    self.root.after(50, self.animate_gif)  # Use a fixed delay for simplicity
                    
            
            

    def update_display(self, temperature, humidity,percentage):
            self.temperature_display.config(text=f"{temperature:.1f} \u00B0C")
            self.humidity_display.config(text=f"{humidity:.1f}%")
            self.log_message(f"Temperature: {temperature:.1f} \u00B0C, Humidity: {humidity:.1f}%")
            self.log_message(f"Water Level: {percentage:.1f}%")
            self.log_message("PH Value: 7.4")
            # Additional logic to update water level and pH value can be added here

            # Update the water level display
            self.water_level_bar['value'] = percentage  # Sets the progress bar to the current percentage
            self.water_level_value.config(text=f"{percentage:.1f}%")  # Updates the text label to show the percentage
            
            self.ph_value_display.config(text="7.4")
            

    def fetch_data(self):
        while True:
            if not self.fetching_active:
                break  # Exit the loop if fetching is stopped
            try:
                # Fetch data from the weather URL
                weather_response = requests.get(self.weather_url)
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    temperature = weather_data['current']['temperature_2m']
                    humidity = weather_data['current']['relative_humidity_2m']

                    # Fetch data from the percentage URL
                    percentage_response = requests.get(self.percentage_url)
                    if percentage_response.status_code == 200:
                        percentage_data = percentage_response.json()
                        percentage = percentage_data.get("percentage", 0)
                    else:
                        percentage = 0  # Default to 0 if there's an error

                    # Update the display with temperature, humidity, and percentage
                    self.update_display(temperature, humidity, percentage)
                else:
                    self.log_message(f"Error fetching weather data: {weather_response.status_code}")

            except Exception as e:
                self.log_message(f"Error: {e}")

            time.sleep(10)  # Adjust the sleep time as necessary



    def start_fetching(self):
        if not self.fetching_active:  # Only start if not already active
            self.fetching_active = True
            self.log_message("Started fetching data.")
            threading.Thread(target=self.fetch_data, daemon=True).start()
        

    def stop_fetching(self):
        self.fetching_active = False
        self.log_message("Stopped fetching data.")
        self.update_display(0.0, 0.0, 0.0)  # Reset the display to 0 values

    

    def log_message(self, message):
        self.log_text_area.insert(tk.END, message + '\n')
        self.log_text_area.yview(tk.END)  # Auto-scroll to the bottom

if __name__ == "__main__":
    root = tk.Tk()
    hydroponic_ui = HydroponicUI(root) 
