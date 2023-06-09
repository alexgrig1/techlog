import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from tkinter import colorchooser
import psutil
import ctypes
import pystray
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from tkinter import filedialog

SPI_SETMOUSESPEED = 0x0071
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02


def check_credentials(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                   (username, password))
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
        show_main_window(user_id, time_remaining, app)
    else:
        messagebox.showerror("Login failed", "Incorrect username or password")


# Choose Color
def color_change(window):
    color = colorchooser.askcolor()
    colorname = color[1]
    window.configure(background=colorname)


# Set Backgrounds
def browseFiles():
    filename = filedialog.askopenfilename(
        initialdir=str(Path.home() / "Desktop"),
        title="Select a File",
        filetypes=(("Text files",
                    "*.jpg;*.jpeg;*.png;*.gif"),
                   ("all files",
                    "*.*")))
    if filename and is_image_file(filename):
        set_desktop_background(filename)


def is_image_file(filename):
    try:
        img = Image.open(filename)
        img.close()
        return True
    except (IOError, OSError):
        return False


def set_desktop_background(image_file):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0,
                                               os.path.abspath(image_file), 0)


def set_mouse_speed(speed):
    user32 = ctypes.windll.user32
    user32.SystemParametersInfoW(SPI_SETMOUSESPEED, 0, speed,
                                 SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)


def on_mouse_speed_change(value):
    speed = int(float(value))
    set_mouse_speed(speed)


def create_system_tray_icon(widget_manager_window, app):
    # Set the font for the widget text
    font = ImageFont.truetype('arial.ttf', 12)

    # Set the widget text colors
    text_color = (255, 255, 255)

    # Create the tray icon image
    image = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), 'W', font=font, fill=text_color)

    # Create the tray icon
    icon = pystray.Icon('widget_icon', image, 'Widgets')
    icon.visible = False

    # Hide the window
    widget_manager_window.withdraw()

    # Define a function to restore the window when the tray icon is clicked
    def restore_window(icon, item):
        # Show the window
        widget_manager_window.deiconify()

        # Remove the tray icon
        icon.stop()

    # Deiconify the app (!bug runs without an icon)
    def exit_app():
        icon.stop()
        widget_manager_window.quit()
        app.quit()

    # Add a menu item to the tray icon to restore the window
    icon.menu = pystray.Menu(
        pystray.MenuItem('Show Widget Manager', restore_window),
        pystray.MenuItem('Exit', exit_app))

    # Run the system tray event loop
    icon.run()


def on_window_drag(event, window):
    x, y = event.x_root, event.y_root
    window.geometry(f"+{x}+{y}")


def show_main_window(user_id, time_remaining, app):
    app.withdraw()  # Hide the login window

    def do_nothing():
        pass

    app.protocol("WM_DELETE_WINDOW",
                 do_nothing)  # Prevent closing with 'x' button

    def show_login_window():
        mouse_sensitivity_window.destroy()
        hardware_usage_window.destroy()
        widget_manager_window.destroy()
        app.protocol("WM_DELETE_WINDOW",
                     do_nothing)  # Prevent closing with 'x' button
        app.deiconify()  # Show the login window

    def close_widget_manager_window():
        create_system_tray_icon(widget_manager_window, app)

    # Gui For themes
    def change_theme(theme):
        global style
        style.theme_use(theme)

    global style
    themes = ttk.Style().theme_names()

    theme_variable = tk.StringVar()
    theme_variable.set(themes[0])

    # Mouse Sensitivity window
    mouse_sensitivity_window = tk.Toplevel()
    mouse_sensitivity_window.title("Mouse Sensitivity")
    mouse_sensitivity_window.withdraw()  # Hide the window initially
    mouse_sensitivity_window.protocol("WM_DELETE_WINDOW",
                                      do_nothing)  # Prevent closing with 'x' button
    mouse_sensitivity_window.overrideredirect(
        True)  # Remove window decorations and taskbar entry

    # Create a draggable frame inside the Mouse Sensitivity window
    draggable_frame = ttk.Frame(mouse_sensitivity_window)
    draggable_frame.pack()
    draggable_frame.bind('<B1-Motion>', lambda event: on_window_drag(event,
                                                                     mouse_sensitivity_window))

    mouse_speed_label = ttk.Label(draggable_frame, text="Mouse Speed")
    mouse_speed_label.pack()
    mouse_speed_slider = ttk.Scale(draggable_frame, from_=1, to=20,
                                   orient="horizontal", length=200,
                                   command=on_mouse_speed_change)
    mouse_speed_slider.set(10)
    mouse_speed_slider.pack()

    # CLOCK
    clock_usage = tk.Toplevel()
    clock_usage.title("CLOCK")
    clock_usage.withdraw()
    clock_usage.protocol("WM_DELETE_WINDOW",
                         do_nothing)
    clock_usage.overrideredirect(True)

    clock_label = ttk.Label(clock_usage, font=("Arial", 16))
    clock_label.pack()

    # Chage Color with right-clck
    clock_usage.bind('<Button-3>', lambda event: color_change(clock_label))

    clock_usage.bind('<B1-Motion>',
                     lambda event: on_window_drag(event,
                                                  clock_usage))
    # Hardware Usage window
    hardware_usage_window = tk.Toplevel()
    hardware_usage_window.title("Hardware Usage")
    hardware_usage_window.withdraw()  # Hide the window initially
    hardware_usage_window.protocol("WM_DELETE_WINDOW",
                                   do_nothing)  # Prevent closing with 'x' button
    hardware_usage_window.overrideredirect(
        True)  # Remove window decorations and taskbar entry

    time_remaining_var = tk.StringVar()
    time_remaining_var.set(f"Time remaining: {int(time_remaining)} seconds")
    time_remaining_label = tk.Label(hardware_usage_window,
                                    textvariable=time_remaining_var)
    time_remaining_label.pack()

    def update_database(value):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Perform the necessary database update based on your requirements
        cursor.execute(
            "UPDATE users SET time_remaining = ? WHERE username = ?",
            (value, 'employee'))
        conn.commit()

        conn.close()

    def reduce_time_remaining(value, time_remaining_var):
        if value <= 0:
            return

        value -= 1
        time_remaining_var.set(f"Time remaining: {value} seconds")
        update_database(value)
        time_remaining_label.after(1000, reduce_time_remaining, value,
                                   time_remaining_var)

    reduce_time_remaining(time_remaining, time_remaining_var)

    cpu_ram_gpu_usage_var = tk.StringVar()
    cpu_ram_gpu_usage_label = ttk.Label(hardware_usage_window,
                                        textvariable=cpu_ram_gpu_usage_var)
    cpu_ram_gpu_usage_label.pack()

    # Make the Hardware Usage window draggable
    hardware_usage_window.bind('<B1-Motion>',
                               lambda event: on_window_drag(event,
                                                            hardware_usage_window))


    def update_cpu_ram_usage():
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
        cpu_ram_gpu_usage_var.set(
            f"CPU: {cpu_percent}% | RAM: {ram_percent}% ")
        hardware_usage_window.after(1000, update_cpu_ram_usage)

    update_cpu_ram_usage()

    # Widget Manager window
    widget_manager_window = tk.Toplevel()
    widget_manager_window.title("Widget Manager")
    widget_manager_window.protocol("WM_DELETE_WINDOW",
                                   close_widget_manager_window)

    hardware_usage_var = tk.BooleanVar()
    mouse_sensitivity_var = tk.BooleanVar()
    clock_var = tk.BooleanVar()

    def toggle_hardware_usage_window():
        if hardware_usage_var.get():
            hardware_usage_window.deiconify()
        else:
            hardware_usage_window.withdraw()

    def toggle_mouse_sensitivity_window():
        if mouse_sensitivity_var.get():
            mouse_sensitivity_window.deiconify()
        else:
            mouse_sensitivity_window.withdraw()

    def toggle_clock():
        if clock_var.get():
            clock_usage.deiconify()
            update_clock()
        else:
            clock_usage.withdraw()

    hardware_usage_checkbutton = ttk.Checkbutton(widget_manager_window,
                                                 text="Hardware Usage",
                                                 variable=hardware_usage_var,
                                                 command=toggle_hardware_usage_window)
    hardware_usage_checkbutton.grid(row=0, column=0)

    mouse_sensitivity_checkbutton = ttk.Checkbutton(widget_manager_window,
                                                    text="Mouse Sensitivity",
                                                    variable=mouse_sensitivity_var,
                                                    command=toggle_mouse_sensitivity_window)
    mouse_sensitivity_checkbutton.grid(row=1, column=0)

    clock_checkbutton = ttk.Checkbutton(widget_manager_window,
                                        text="Clock",
                                        variable=clock_var,
                                        command=toggle_clock)
    clock_checkbutton.grid(row=2, column=0)

    # Choose background
    background_button = ttk.Button(widget_manager_window,
                                   text="Choose Your Desktop",
                                   command=browseFiles
                                   )
    background_button.grid(row=3, column=0)

    # Change themes
    theme_label = ttk.Label(widget_manager_window, text="Select Theme:")
    theme_label.grid(row=0, column=1)
    theme_dropdown = ttk.OptionMenu(widget_manager_window, theme_variable,
                                    *themes, command=change_theme)
    theme_dropdown.grid(row=1, column=1)

    style = ttk.Style()

    def update_clock():
        current_time = datetime.now().strftime("%H:%M:%S")
        clock_label.config(text=current_time)
        widget_manager_window.after(1000, update_clock)

    logout_button = ttk.Button(widget_manager_window, text="Logout",
                               command=show_login_window)
    logout_button.grid(row=6, column=0)

    # Close all widget windows when the main application is closed
    app.protocol("WM_DELETE_WINDOW", app.quit)

# app.mainloop()
