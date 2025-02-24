import sqlite3
import bcrypt

def iniciar_bd():
    conector = sqlite3.connect("users.bd")
    cursor = conector.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conector.commit()
    conector.close()