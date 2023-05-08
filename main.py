app = tk.Tk()
app.title("Login App")

# Create labels, entries, and radio buttons
username_label = tk.Label(app, text="Username:")
username_entry = tk.Entry(app)
password_label = tk.Label(app, text="Password:")
password_entry = tk.Entry(app, show="*")
user_type_var = tk.StringVar()
employee_rb = tk.Radiobutton(app, text="Employee", variable=user_type_var, value="Employee")
customer_rb = tk.Radiobutton(app, text="Customer", variable=user_type_var, value="Customer")
login_button = tk.Button(app, text="Login", command=login)

# Position the elements using grid layout
username_label.grid(row=0, column=0)
username_entry.grid(row=0, column=1)
password_label.grid(row=1, column=0)
password_entry.grid(row=1, column=1)
employee_rb.grid(row=2, column=0)
customer_rb.grid(row=2, column=1)
login_button.grid(row=3, column=1, sticky="E")

# Start the main event loop
app.mainloop()