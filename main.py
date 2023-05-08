import tkinter as tk
import sqlite3
from tkinter import messagebox
from Functions import *


app = tk.Tk()
app.title("Login App")

app.protocol('WM_DELETE_WINDOW', lambda: None)  #

# Create labels, entries, and radio buttons
username_label = tk.Label(app, text="Username:")
username_entry = tk.Entry(app)
password_label = tk.Label(app, text="Password:")
password_entry = tk.Entry(app, show="*")
login_button = tk.Button(app, text="Login", command=lambda: login(username_entry, password_entry, app))

# Position the elements using grid layout
username_label.grid(row=0, column=0)
username_entry.grid(row=0, column=1)
password_label.grid(row=1, column=0)
password_entry.grid(row=1, column=1)
login_button.grid(row=3, column=1, sticky="E")


# Start the main event loop
app.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable the close button
app.mainloop()
