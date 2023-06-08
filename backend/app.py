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


def get_username(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
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
    user_id = get_username(username)
    if user_id:
        return jsonify({'error': 'Username already exists'}), 400
    else:
        cursor.execute("INSERT INTO users (username, password, face_data) VALUES (?, ?, ?)",
                       (username, hashed_password, photo_data))

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

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user[1]):
        return jsonify({'error': 'Invalid username or password'}), 401

    # create JWT token
    token = jwt.encode({'username': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                       app.config['SECRET_KEY'])

    token_base64 = base64.b64encode(token.encode('utf-8')).decode('utf-8')
    return jsonify({'token': token_base64})


# Hàm xử lý ảnh blob và so sánh khuôn mặt
def compare_faces(image_known, image_unknown):
    known_encoding = face_recognition.face_encodings(image_known)[0]
    unknown_encoding = face_recognition.face_encodings(image_unknown)[0]

    results = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=0.5)
    return results[0]


@app.route('/api/loginFace', methods=['POST'])
def login_face():
    data = request.get_json()
    username = data['username']
    photo_data = data['photo']
    image_unknown = base64_to_image(photo_data)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    auth = False

    if user:
        blob = user[2]

        image_known = blob_to_image(blob)

        auth = compare_faces(image_known, image_unknown)

    conn.close()

    token = jwt.encode({'username': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
    if auth:
        token_base64 = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        return jsonify({'token': token_base64})
    else:
        return jsonify({'token': False})


# Hàm chuyển đổi Base64 thành ảnh numpy array
def base64_to_image(base64_data):
    image_data = base64.b64decode(base64_data)
    image_np = np.frombuffer(image_data, dtype=np.uint8)
    image_rgb = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    return image_rgb


# Hàm chuyển đổi blob thành ảnh numpy array
def blob_to_image(blob):
    arr = np.frombuffer(blob, dtype=np.uint8)
    image_rgb = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return image_rgb


if __name__ == '__main__':
    app.run()
