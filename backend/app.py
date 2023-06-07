from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import bcrypt
import jwt
import datetime
import secrets
import base64
import face_recognition
import cv2
import numpy as np

app = Flask(__name__)
DATABASE = 'users.db'
CORS(app)
app.config['SECRET_KEY'] = secrets.token_hex(16)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


def get_user_id(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None


@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    photo_data = request.json.get('photo')
    photo_data = base64.b64decode(photo_data)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # check if user already exists
    user_id = get_user_id(username)
    if user_id:
        return jsonify({'error': 'Username already exists'}), 400
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, hashed_password))
        user_id = cursor.lastrowid

    cursor.execute("INSERT INTO faces (user_id, face_data) VALUES (?, ?)",
                   (user_id, photo_data))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Registration successful'})


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # get user from database
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user[2]):
        return jsonify({'error': 'Invalid username or password'}), 401

    # create JWT token
    token = jwt.encode({'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                       app.config['SECRET_KEY'])

    token_base64 = base64.b64encode(token.encode('utf-8')).decode('utf-8')
    return jsonify({'token': token_base64})


@app.route('/api/loginFace', methods=['POST'])
def login_face():
    data = request.get_json()
    username = data['username']
    photo_data = request.json.get('photo')
    photo_data = base64.b64decode(photo_data)
    image_np = np.frombuffer(photo_data, dtype=np.uint8)
    image_unknown = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()


    auth = False

    if user:
        cursor.execute('SELECT face_data FROM faces WHERE user_id = ?', (user[0],))
        user_face = cursor.fetchone()
        blob = user_face[0]

        # Chuyển đổi blob thành hình ảnh
        arr = np.frombuffer(blob, dtype=np.uint8)
        image_known = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        auth = init_face(image_known, image_unknown)

    token_base64 = ""
    if auth:
        # create JWT token
        token = jwt.encode({'user_id': user[1], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                           app.config['SECRET_KEY'])

        token_base64 = base64.b64encode(token.encode('utf-8')).decode('utf-8')
    conn.close()

    return jsonify({'token': token_base64})


def init_face(image_known, image_unknown):
    know_encoding = face_recognition.face_encodings(image_known)[0]
    unknown_encoding = face_recognition.face_encodings(image_unknown)[0]

    results = face_recognition.compare_faces([know_encoding], unknown_encoding, tolerance=0.6)
    return results


if __name__ == '__main__':
    app.run()
