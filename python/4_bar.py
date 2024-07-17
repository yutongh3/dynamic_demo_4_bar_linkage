import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

def refresh_ports():
    port_combobox['values'] = [port.device for port in serial.tools.list_ports.comports()]
    if port_combobox['values']:
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
            check_connection()
        except serial.SerialException as e:
            result_label.config(text=f"Failed to connect to {port}: {e}")
    else:
        result_label.config(text="Please select a COM port")

def send_command(command):
    if ser:
        try:
            ser.write((command + '\n').encode())
            # print(f"Sent command: {command}")
            result_label.config(text=f"Command sent: {command}")
        except serial.SerialException as e:
            result_label.config(text=f"Failed to send command: {e}")
    else:
        result_label.config(text="Serial connection not established")

def on_stop():
    send_command("STOP")

def enable_controls(enable):
    state = tk.NORMAL if enable else tk.DISABLED
    for widget in control_widgets:
        widget.config(state=state)

def check_connection():
    if ser:
        try:
            ser.readline()
            root.after(1000, check_connection)
        except serial.SerialException:
            result_label.config(text="Connection lost. Please reconnect.")
            enable_controls(False)

root = tk.Tk()
root.title("Servo Control Panel")
ser = None

ttk.Label(root, text="Select a COM port:").pack(padx=10, pady=5)
port_combobox = ttk.Combobox(root, width=50, state="readonly")
port_combobox.pack(padx=10, pady=5)
ttk.Button(root, text="Refresh Ports", command=refresh_ports).pack(padx=10, pady=5)
ttk.Button(root, text="Connect", command=connect_to_port).pack(padx=10, pady=5)

direction_combobox = ttk.Combobox(root, width=10, state="readonly", values=["CW", "CCW"])
direction_combobox.pack(padx=10, pady=5)
direction_combobox.set("CW")  # Set default value

speed_combobox = ttk.Combobox(root, width=10, state="readonly", values=["75", "100"])
speed_combobox.pack(padx=10, pady=5)
speed_combobox.set("75")  # Set default value

control_frame = ttk.Frame(root)
control_frame.pack(padx=10, pady=10)

send_button = ttk.Button(control_frame, text="Go", command=lambda: send_command(f"{direction_combobox.get()} {speed_combobox.get()}"))
send_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(control_frame, text="Stop", command=on_stop)
stop_button.pack(side=tk.LEFT, padx=10)

control_frame = ttk.Frame(root)
control_frame.pack(padx=10, pady=15)

angles = ["0deg", "90deg", "180deg", "270deg"]
for angle in angles:
    button = ttk.Button(control_frame, text=angle, command=lambda a=angle: send_command(a))
    button.pack(side=tk.LEFT, padx=10)

control_frame = ttk.Frame(root)
control_frame.pack(padx=10, pady=20)

commends = ["forward", "backward"]
for commend in commends:
    button = ttk.Button(control_frame, text=commend, command=lambda a=commend: send_command(a))
    button.pack(side=tk.LEFT, padx=10)

result_label = ttk.Label(root, text="")
result_label.pack(padx=10, pady=10)

refresh_ports()
control_widgets = [direction_combobox, speed_combobox, send_button, stop_button] + control_frame.winfo_children()
enable_controls(False)

root.mainloop()
