# database.py
import sqlite3

def create_tables():
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER,
                        gender TEXT,  -- Added gender column
                        address TEXT,
                        symptoms TEXT
                    )''')

    connection.commit()
    connection.close()

def add_user(username, password, role):
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    connection.commit()
    connection.close()

def get_user(username, password):
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    connection.close()
    return user
