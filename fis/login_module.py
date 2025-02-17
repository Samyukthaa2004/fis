import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import io

# Database setup
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        image BLOB
    )
''')
conn.commit()


# Function to load logo
def load_logo():
    try:
        img = Image.open("logo.png")  # Make sure logo.png exists
        img = img.resize((100, 100))
        logo_img = ImageTk.PhotoImage(img)
        logo_label.config(image=logo_img)
        logo_label.image = logo_img  # Keep reference
    except Exception as e:
        print("Logo not found!", e)


# Function to select user profile image
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        with open(file_path, "rb") as file:
            global user_image_data
            user_image_data = file.read()

        img = Image.open(file_path)
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)
        profile_label.config(image=img)
        profile_label.image = img


# Function to register user
def register():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password or user_image_data is None:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, image) VALUES (?, ?, ?)",
                       (username, password, user_image_data))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "User Registered Successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")


# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT image FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Login Success", f"Welcome, {username}")

        # Load stored profile image
        image_data = user[0]
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((100, 100))
        profile_img = ImageTk.PhotoImage(image)

        profile_label.config(image=profile_img)
        profile_label.image = profile_img  # Keep reference
    else:
        messagebox.showerror("Login Failed", "Invalid Credentials")


# Initialize Tkinter Window
root = tk.Tk()
root.title("User Authentication")
root.geometry("400x550")

# Load Logo
logo_label = tk.Label(root, text="App Logo", bg="gray", width=15, height=7)
logo_label.pack(pady=10)
load_logo()

# Profile Image Placeholder
user_image_data = None
profile_label = tk.Label(root, text="Profile Image", bg="gray", width=15, height=7)
profile_label.pack(pady=10)

# Select Profile Image Button
btn_select_image = tk.Button(root, text="Choose Profile Image", command=select_image)
btn_select_image.pack(pady=5)

# Username Entry
tk.Label(root, text="Username:").pack(pady=(10, 0))
entry_username = tk.Entry(root, width=30)
entry_username.pack(pady=5)

# Password Entry
tk.Label(root, text="Password:").pack(pady=(10, 0))
entry_password = tk.Entry(root, width=30, show="*")
entry_password.pack(pady=5)

# Register Button
btn_register = tk.Button(root, text="Register", command=register, bg="green", fg="white")
btn_register.pack(pady=5)

# Login Button
btn_login = tk.Button(root, text="Login", command=login, bg="blue", fg="white")
btn_login.pack(pady=10)

root.mainloop()
