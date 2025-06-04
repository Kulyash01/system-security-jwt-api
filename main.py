from flask import Flask, request, jsonify
import jwt
import datetime
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
secret_key = os.environ.get('SECRET_KEY')
if not secret_key:
    raise RuntimeError("SECRET_KEY environment variable not set")
app.config['SECRET_KEY'] = secret_key


def load_credentials():
    """Load user credentials from a JSON file or environment variables."""
    cred_file = os.environ.get('CREDENTIALS_FILE')
    username = os.environ.get('USERNAME')
    password_hash = os.environ.get('PASSWORD_HASH')
    password = os.environ.get('PASSWORD')

    if cred_file and os.path.exists(cred_file):
        with open(cred_file) as f:
            data = json.load(f)
            username = username or data.get('username')
            password_hash = password_hash or data.get('password_hash')
            if not password_hash and data.get('password'):
                password_hash = generate_password_hash(data['password'])

    if not password_hash and password:
        password_hash = generate_password_hash(password)

    if not username or not password_hash:
        raise RuntimeError('User credentials not provided')

    return username, password_hash


STORED_USERNAME, STORED_PASSWORD_HASH = load_credentials()

# Roles that are permitted to access protected resources
ALLOWED_ROLES = {"admin", "user"}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    # Use provided role if valid; otherwise fall back to the default "admin" role
    role = data.get('role', 'admin')
    if role not in ALLOWED_ROLES:
        role = 'admin'

    if username == STORED_USERNAME and check_password_hash(STORED_PASSWORD_HASH, password):
        token = jwt.encode({
            'user': username,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'message': 'Missing or invalid token'}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

        if payload.get('role') not in ALLOWED_ROLES:
            return jsonify({'message': 'Access forbidden: Admins or users only'}), 403

        return jsonify({'message': 'Access granted'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    debug_env = os.environ.get('FLASK_DEBUG', '0')
    debug_mode = debug_env.lower() in ('1', 'true', 't', 'yes')
    app.run(debug=debug_mode)

