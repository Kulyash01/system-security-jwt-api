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

# Roles that are permitted to access protected resources
ALLOWED_ROLES = {"admin", "user"}


def load_credentials():
    """Load user credentials from a JSON file or environment variables."""
    cred_file = os.environ.get('CREDENTIALS_FILE')
    username = os.environ.get('USERNAME')
    password_hash = os.environ.get('PASSWORD_HASH')
    password = os.environ.get('PASSWORD')
    role = os.environ.get('ROLE')

    if cred_file and os.path.exists(cred_file):
        with open(cred_file) as f:
            data = json.load(f)
            username = username or data.get('username')
            password_hash = password_hash or data.get('password_hash')
            if not password_hash and data.get('password'):
                password_hash = generate_password_hash(data['password'])
            role = role or data.get('role')

    if not password_hash and password:
        password_hash = generate_password_hash(password)

    if role is None:
        role = 'admin'
    elif role not in ALLOWED_ROLES:
        raise RuntimeError('Invalid role')

    if not username or not password_hash:
        raise RuntimeError('User credentials not provided')

    return username, password_hash, role


STORED_USERNAME, STORED_PASSWORD_HASH, STORED_ROLE = load_credentials()

# In-memory store of registered users. Starts with the credentials loaded from
# the environment or credential file.
USERS = {
    STORED_USERNAME: {
        'password_hash': STORED_PASSWORD_HASH,
        'role': STORED_ROLE,
    }
}


@app.route('/register', methods=['POST'])
def register():
    """Register a new user with a username, password and optional role."""
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    if username in USERS:
        return jsonify({'message': 'User already exists'}), 400

    if role not in ALLOWED_ROLES:
        return jsonify({'message': 'Invalid role'}), 400

    USERS[username] = {
        'password_hash': generate_password_hash(password),
        'role': role,
    }

    return jsonify({'message': 'User registered'}), 201

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'message': 'Invalid or missing JSON payload'}), 400

    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    user = USERS.get(username)
    # Ignore any role provided by the request and use the stored role for the user
    if user and check_password_hash(user['password_hash'], password):
        token = jwt.encode({
            'user': username,
            'role': user['role'],
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

