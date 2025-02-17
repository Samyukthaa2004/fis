import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Install with: pip install pillow

def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect("faculty_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Login Success", f"Welcome, {username}")
        root.destroy()
        if user[0] == "admin":
            import department_module  # Open Department Selection
            department_module.department_window()
        else:
            import faculty_module  # Open Faculty List
            faculty_module.faculty_list_window()
    else:
        messagebox.showerror("Login Failed", "Invalid Credentials")

# Tkinter UI for Login
root = tk.Tk()
root.title("Login Page")
root.geometry("400x500")
root.configure(bg="lightgray")

# Load and display the logo/image
logo_path = "logo.png"  # Ensure you have an image named 'logo.png' in the same directory
try:
    img = Image.open(logo_path)
    img = img.resize((120, 120), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    logo_label = tk.Label(root, image=img, bg="lightgray")
    logo_label.pack(pady=10)
except Exception as e:
    print("Error loading image:", e)

# Username Label & Entry
tk.Label(root, text="Username:", font=("Arial", 12), bg="lightgray").pack(pady=5)
entry_username = tk.Entry(root, font=("Arial", 12))
entry_username.pack(pady=5)

# Password Label & Entry
tk.Label(root, text="Password:", font=("Arial", 12), bg="lightgray").pack(pady=5)
entry_password = tk.Entry(root, font=("Arial", 12), show="*")  # Mask password input
entry_password.pack(pady=5)

# Login Button
tk.Button(root, text="Login", font=("Arial", 12), bg="blue", fg="white", command=login).pack(pady=10)

root.mainloop()

