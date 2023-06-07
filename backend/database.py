import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# create table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')

cursor.execute('''
    CREATE TABLE faces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        face_data TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

conn.commit()
conn.close()