import sqlite3
import tkinter as tk
from tkinter import messagebox
import psutil
import ctypes


# Constants for changing the mouse speed
SPI_SETMOUSESPEED = 0x0071
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02


def check_credentials(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0], result[4]  # Return user ID and time_remaining
    else:
        return None



def login(username_entry, password_entry, app):
    username = username_entry.get()
    password = password_entry.get()

    result = check_credentials(username, password)

    if result:
        user_id, time_remaining = result
        messagebox.showinfo("Login successful", f"Welcome, {username}!")
        app.destroy()  # Close the login window
        show_main_window(user_id, time_remaining)
    else:
        messagebox.showerror("Login failed", "Incorrect username or password")

# Function to change the mouse speed
def set_mouse_speed(speed):
    user32 = ctypes.windll.user32
    user32.SystemParametersInfoW(SPI_SETMOUSESPEED, 0, speed, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)


# Function to handle changes to the mouse speed slider
def on_mouse_speed_change(value):
    set_mouse_speed(int(value))


def show_main_window(user_id, time_remaining):
    main_app = tk.Tk()
    main_app.title("Main App")



    # Create the mouse speed slider
    mouse_speed_label = tk.Label(main_app, text="Mouse Speed")
    mouse_speed_label.pack()
    mouse_speed_slider = tk.Scale(main_app, from_=1, to=20, orient="horizontal", length=200)
    mouse_speed_slider.set(10)
    mouse_speed_slider.pack()

    mouse_speed_slider.config(command=on_mouse_speed_change)

    time_remaining_var = tk.StringVar()
    time_remaining_var.set(f"Time remaining: {time_remaining} seconds")

    time_remaining_label = tk.Label(main_app, textvariable=time_remaining_var)
    time_remaining_label.pack()

    cpu_ram_usage_var = tk.StringVar()

    cpu_ram_usage_label = tk.Label(main_app, textvariable=cpu_ram_usage_var)
    cpu_ram_usage_label.pack()

    def update_cpu_ram_usage():
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent

        cpu_ram_usage_var.set(f"CPU: {cpu_percent}% | RAM: {ram_percent}%")

        main_app.after(1000, update_cpu_ram_usage)

    update_cpu_ram_usage()

    main_app.mainloop()