import sqlite3

conn = sqlite3.connect("faculty_management.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS departments (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
cursor.execute("CREATE TABLE IF NOT EXISTS faculty (id INTEGER PRIMARY KEY, name TEXT, dob TEXT, email TEXT, experience TEXT, designation TEXT, department_id INTEGER, FOREIGN KEY(department_id) REFERENCES departments(id))")
cursor.execute("CREATE TABLE IF NOT EXISTS faculty_data (id INTEGER PRIMARY KEY, faculty_id INTEGER, achievements TEXT, personal_details TEXT, responsible_class TEXT, joining_date TEXT, passcode TEXT, FOREIGN KEY(faculty_id) REFERENCES faculty(id))")

conn.commit()
conn.close()

print("Database setup complete!")
