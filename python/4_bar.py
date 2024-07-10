import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

def refresh_ports():
    port_combobox['values'] = []
    ports = serial.tools.list_ports.comports()
    port_combobox['values'] = [port.device for port in ports]
    if ports:
        port_combobox.current(0)
    else:
        port_combobox.set('No COM ports found')

def connect_to_port():
    port = port_combobox.get()
    if port:
        try:
            global ser
            ser = serial.Serial(port, 9600, timeout=1)
            result_label.config(text=f"Connected successfully to {port}")
            enable_controls(True)
        except serial.SerialException as e:
            result_label.config(text=f"Failed to connect to {port}: {e}")
    else:
        result_label.config(text="Please select a COM port")

def send_command(command):
    if ser:
        ser.write(command.encode())
    else:
        result_label.config(text="Serial connection not established")

def on_slider_change(value):
    command = str(int(float(value)))  # Convert the slider value to integer string
    if ser:
        ser.write(command.encode())
        result_label.config(text=f"speed set to: {command}")
    else:
        result_label.config(text="Serial connection not established")

def enable_controls(enable):
    if enable:
        for button in control_buttons:
            button.config(state=tk.NORMAL)
        slider.config(state=tk.NORMAL)
    else:
        for button in control_buttons:
            button.config(state=tk.DISABLED)
        slider.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("COM Port Connector")

# Create and pack the widgets
ttk.Label(root, text="Select a COM port:").pack(padx=10, pady=5)
port_combobox = ttk.Combobox(root, width=50, state="readonly")
port_combobox.pack(padx=10, pady=5)
refresh_button = ttk.Button(root, text="Refresh Ports", command=refresh_ports)
refresh_button.pack(padx=10, pady=5)
connect_button = ttk.Button(root, text="Connect", command=connect_to_port)
connect_button.pack(padx=10, pady=5)

# Control buttons
buttons_frame = ttk.Frame(root)
buttons_frame.pack(padx=10, pady=10)
control_buttons = []
for command in ["Left", "Stop", "Right"]:
    button = ttk.Button(buttons_frame, text=command, command=lambda cmd=command: send_command(cmd))
    button.pack(side=tk.LEFT, padx=5)
    control_buttons.append(button)

# Slider for sending values 0-100
slider = tk.Scale(root, from_=0, to=100, orient='horizontal', command=on_slider_change)
slider.pack(fill=tk.X, padx=10, pady=10)
slider.config(state=tk.DISABLED)

result_label = ttk.Label(root, text="")
result_label.pack(padx=10, pady=10)

# Initialize the port list and disable control buttons
refresh_ports()
enable_controls(False)

# Start the GUI
root.mainloop()
