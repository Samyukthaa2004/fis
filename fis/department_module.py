import sqlite3
import tkinter as tk
from tkinter import ttk

def department_window():
    def select_department():
        selected_dept = dept_combobox.get()
        if selected_dept:
            root.destroy()
            import faculty_module
            faculty_module.faculty_list_window(selected_dept)

    conn = sqlite3.connect("faculty_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM departments")
    departments = [row[0] for row in cursor.fetchall()]
    conn.close()

    root = tk.Tk()
    root.title("Select Department")
    root.geometry("400x200")

    tk.Label(root, text="Select a Department:").pack()
    dept_combobox = ttk.Combobox(root, values=departments)
    dept_combobox.pack()

    tk.Button(root, text="Proceed", command=select_department).pack()

    root.mainloop()
