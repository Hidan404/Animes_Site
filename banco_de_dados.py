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


def registrar_usuario(username,passwd):
    conector = sqlite3.connect("users.bd")
    cursor = conector.cursor()
    hashed = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('''
    INSERT INTO users (username, password) VALUES (?, ?)
    ''', (username, hashed))
    conector.commit()
    conector.close()