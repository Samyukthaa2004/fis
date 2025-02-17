import sqlite3
import tkinter as tk
from tkinter import ttk


def faculty_list_window(department):
    root = tk.Tk()
    root.title(f"Faculty of {department}")
    root.geometry("600x400")

    tree = ttk.Treeview(root, columns=("Name", "DOB", "Email", "Experience", "Designation"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("DOB", text="Date of Birth")
    tree.heading("Email", text="Email")
    tree.heading("Experience", text="Experience")
    tree.heading("Designation", text="Designation")
    tree.pack(fill="both", expand=True)

    conn = sqlite3.connect("faculty_management.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, dob, email, experience, designation FROM faculty 
        WHERE department_id = (SELECT id FROM departments WHERE name = ?)
    """, (department,))

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    conn.close()
    root.mainloop()
