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
            ser = serial.Serial(port, 115200, timeout=1)
            result_label.config(text=f"Connected successfully to {port}")
            enable_controls(True)
        except serial.SerialException as e:
            result_label.config(text=f"Failed to connect to {port}: {e}")
    else:
        result_label.config(text="Please select a COM port")

def send_command(command):
    if ser:
        ser.write(command.encode())
        print(f"Sent command: {command}")
        result_label.config(text=f"Speed set to: {command}")
    else:
        result_label.config(text="Serial connection not established")

def on_slider_change(value):
    global slider_timer
    if slider_timer:
        root.after_cancel(slider_timer)
    slider_timer = root.after(300, send_command, str(int(float(value))))

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
slider_timer = None

ttk.Label(root, text="Select a COM port:").pack(padx=10, pady=5)
port_combobox = ttk.Combobox(root, width=50, state="readonly")
port_combobox.pack(padx=10, pady=5)
refresh_button = ttk.Button(root, text="Refresh Ports", command=refresh_ports)
refresh_button.pack(padx=10, pady=5)
connect_button = ttk.Button(root, text="Connect", command=connect_to_port)
connect_button.pack(padx=10, pady=5)

buttons_frame = ttk.Frame(root)
buttons_frame.pack(padx=10, pady=10)
control_buttons = []
for command in ["CW", "Stop", "CCW"]:
    button = ttk.Button(buttons_frame, text=command, command=lambda cmd=command: send_command(cmd))
    button.pack(side=tk.LEFT, padx=5)
    control_buttons.append(button)

slider = tk.Scale(root, from_=0, to=100, orient='horizontal', command=on_slider_change)
slider.pack(fill=tk.X, padx=10, pady=10)
slider.config(state=tk.DISABLED)

result_label = ttk.Label(root, text="")
result_label.pack(padx=10, pady=10)

refresh_ports()
enable_controls(False)

root.mainloop()
