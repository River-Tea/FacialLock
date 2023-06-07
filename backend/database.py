import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# create table
conn.execute('''
    CREATE TABLE users (
        username TEXT PRIMARY KEY,
        password TEXT,
        face_data BLOB
    );
''')


conn.commit()
conn.close()