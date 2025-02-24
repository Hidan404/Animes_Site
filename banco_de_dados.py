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


def login_usuario(username, passwd):
    conector = sqlite3.connect("users.bd")
    cursor = conector.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conector.close()
            
    if result and bcrypt.checkpw(passwd.encode('utf-8'), result[0]):
        return True
    else:
        return False