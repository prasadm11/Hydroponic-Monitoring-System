import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from tkinter import Canvas
from math import pi, cos, sin

class HydroponicGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Hydroponic Monitoring System")
        self.geometry("950x700")
        self.configure(bg='#E3F2FD')

        # Set custom fonts
        self.title_font = tkFont.Font(family="Helvetica", size=26, weight="bold")
        self.label_font = tkFont.Font(family="Arial", size=16, weight="bold")
        self.value_font = tkFont.Font(family="Arial", size=12)

        # Header Section with Gradient Background
        self.header = tk.Frame(self, bg="#4A90E2", padx=20, pady=20)
        self.header.pack(fill=tk.X)

        title = tk.Label(self.header, text="Hydroponic Monitoring System", font=self.title_font, bg="#4A90E2", fg="white")
        title.pack()

        # Tabs for Monitoring and Controls
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Monitoring Tab
        self.monitoring_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.monitoring_tab, text="Monitoring")

        # Controls Tab
        self.controls_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.controls_tab, text="Controls")

        # Apply style for a more modern look
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Style tweaks
        self.style.configure("TNotebook", background="#E3F2FD", borderwidth=0)
        self.style.configure("TNotebook.Tab", padding=(10, 5), font=("Helvetica", 12, "bold"))
        self.style.configure("TLabel", background="#FFFFFF", padding=5)

        # Dark Mode Toggle Button
        self.dark_mode_button = tk.Button(self.header, text="Dark Mode", command=self.toggle_dark_mode,
                                          bg="#5C6BC0", fg="white", font=self.label_font, relief=tk.FLAT, borderwidth=0)
        self.dark_mode_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Create Monitoring and Control widgets
        self.create_monitoring_widgets(self.monitoring_tab)
        self.create_control_widgets(self.controls_tab)

    def create_monitoring_widgets(self, parent):
        # Circular progress bars for pH, temperature, and humidity
        self.create_circular_progress_widget(parent, "pH Level", 6.2, 14, "#FF5252", 120)
        self.create_circular_progress_widget(parent, "Temperature", 24, 50, "#FFCA28", 24)
        self.create_circular_progress_widget(parent, "Humidity", 65, 100, "#66BB6A", 65)

        # Water Level widget with tank design
        self.create_water_level_widget(parent, "Water Level", 70)

    def create_control_widgets(self, parent):
        # Motor controls and sliders
        motor_frame = ttk.LabelFrame(parent, text="Motor Controls", padding=20)
        motor_frame.pack(fill=tk.X, padx=10, pady=10)

        self.create_motor_control(motor_frame, "Water Pump", self.start_water_pump, self.stop_water_pump)
        self.create_motor_control(motor_frame, "Nutrient Pump", self.start_fertilizer_pump, self.stop_fertilizer_pump)

        # Sliders for control with better design
        self.create_slider(parent, "Water Pump Speed", 0, 100, 70)
        self.create_slider(parent, "Nutrient Level", 0, 100, 50)

        # Dropdown Menu for Plant Type Selection
        self.create_dropdown(parent, "Select Plant Type", ["Lettuce", "Tomato", "Basil", "Cucumber"])

    def create_circular_progress_widget(self, parent, label_text, value, max_value, color, progress_value):
        card_frame = tk.Frame(parent, bg="#FFFFFF", padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        card_frame.pack(fill=tk.X, expand=True, pady=10)

        label = tk.Label(card_frame, text=label_text, font=self.label_font, bg="#FFFFFF", fg=color)
        label.pack(anchor='w')

        canvas = tk.Canvas(card_frame, width=150, height=150, bg="#FFFFFF", highlightthickness=0)
        canvas.pack()

        # Drawing the circular progress
        radius = 65
        center_x, center_y = 75, 75
        canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="#B0BEC5", width=15)

        angle = (progress_value / max_value) * 360
        canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius, start=90, extent=-angle, outline=color, width=15, style="arc")

        value_label = tk.Label(card_frame, text=f"{value}/{max_value}", font=self.value_font, bg="#FFFFFF", fg=color)
        value_label.pack()

    def create_water_level_widget(self, parent, label_text, level):
        # Water Level Card
        card_frame = tk.Frame(parent, bg="#FFFFFF", padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        card_frame.pack(fill=tk.X, expand=True, pady=10)

        label = tk.Label(card_frame, text=label_text, font=self.label_font, bg="#FFFFFF", fg="#00BCD4")
        label.pack(anchor='w')

        # Tank Widget using Canvas
        tank_frame = tk.Frame(card_frame, bg="#FFFFFF", padx=20, pady=10)
        tank_frame.pack()

        self.tank_canvas = tk.Canvas(tank_frame, width=100, height=200, bg="#E0E0E0", bd=0, highlightthickness=1, highlightbackground="#B0BEC5")
        self.tank_canvas.pack(side=tk.LEFT)

        # Tank background and water level
        self.tank_canvas.create_rectangle(10, 10, 90, 190, outline="#546E7A", width=2)  # Tank outline
        self.water_level = self.tank_canvas.create_rectangle(10, 190 - (180 * level // 100), 90, 190, fill="#00BCD4")

        self.water_level_label = tk.Label(tank_frame, text=f"{level}%", font=self.value_font, bg="#FFFFFF", fg="#00BCD4")
        self.water_level_label.pack(side=tk.LEFT, padx=10)

    def update_water_level(self, level):
        # Update water level inside the tank
        self.tank_canvas.coords(self.water_level, 10, 190 - (180 * level // 100), 90, 190)
        self.water_level_label.config(text=f"{level}%")

    def create_motor_control(self, parent, label_text, start_cmd, stop_cmd):
        motor_frame = tk.Frame(parent, padx=10, pady=10)
        motor_frame.pack(fill=tk.X, expand=True, pady=10)

        label = tk.Label(motor_frame, text=label_text, font=self.label_font)
        label.pack(anchor='w')

        start_button = tk.Button(motor_frame, text="Start", command=start_cmd, 
                                 bg="#4CAF50", fg="white", font=self.value_font, padx=20, pady=5,
                                 relief=tk.FLAT, borderwidth=0)
        start_button.pack(side=tk.LEFT, padx=5)
        stop_button = tk.Button(motor_frame, text="Stop", command=stop_cmd, 
                                bg="#F44336", fg="white", font=self.value_font, padx=20, pady=5,
                                relief=tk.FLAT, borderwidth=0)
        stop_button.pack(side=tk.RIGHT, padx=5)

    def create_slider(self, parent, label_text, from_, to_, init_value):
        slider_frame = ttk.Frame(parent, padding=10)
        slider_frame.pack(fill=tk.X, expand=True, pady=10)

        label = ttk.Label(slider_frame, text=label_text, font=("Arial", 14))
        label.pack(anchor='w')

        slider = ttk.Scale(slider_frame, from_=from_, to_=to_, orient=tk.HORIZONTAL)
        slider.set(init_value)
        slider.pack(fill=tk.X, expand=True, padx=5)

    def create_dropdown(self, parent, label_text, options):
        dropdown_frame = ttk.Frame(parent, padding=10)
        dropdown_frame.pack(fill=tk.X, expand=True, pady=10)

        label = ttk.Label(dropdown_frame, text=label_text, font=("Arial", 14))
        label.pack(anchor='w')

        dropdown = ttk.Combobox(dropdown_frame, values=options)
        dropdown.current(0)
        dropdown.pack(fill=tk.X, expand=True)

    def start_water_pump(self):
        self.update_water_level(90)

    def stop_water_pump(self):
        self.update_water_level(70)

    def start_fertilizer_pump(self):
        self.update_water_level(80)

    def stop_fertilizer_pump(self):
        self.update_water_level(60)

    def toggle_dark_mode(self):
        if self.cget("bg") == "#E3F2FD":
            self.configure(bg="#212121")
            self.header.configure(bg="#424242")
            self.tab_control.configure(background="#303030")
        else:
            self.configure(bg="#E3F2FD")
            self.header.configure(bg="#4A90E2")
            self.tab_control.configure(background="#E3F2FD")


if __name__ == "__main__":
    app = HydroponicGUI()
    app.mainloop()
