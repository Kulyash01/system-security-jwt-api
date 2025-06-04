import os
import importlib
import datetime
import jwt
import pytest

# Ensure environment variables are set before importing the app
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('USERNAME', 'admin')
os.environ.setdefault('PASSWORD', 'password')
os.environ.setdefault('ROLE', 'admin')

import main
importlib.reload(main)

@pytest.fixture
def client():
    with main.app.test_client() as client:
        yield client


def test_login_success(client):
    resp = client.post('/login', json={'username': 'admin', 'password': 'password'})
    assert resp.status_code == 200
    assert 'token' in resp.get_json()


def test_login_invalid_credentials(client):
    resp = client.post('/login', json={'username': 'admin', 'password': 'wrong'})
    assert resp.status_code == 401
    assert resp.get_json()['message'] == 'Invalid credentials'


def test_login_missing_fields(client):
    resp = client.post('/login', json={'username': 'admin'})
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Username and password required'

    resp = client.post('/login', json={'password': 'password'})
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Username and password required'


def test_login_missing_username(client):
    resp = client.post('/login', json={'password': 'password'})
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Username and password required'


def test_login_missing_password(client):
    resp = client.post('/login', json={'username': 'admin'})
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Username and password required'


def test_login_non_json_payload(client):
    resp = client.post('/login', data='not json', content_type='text/plain')
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Invalid or missing JSON payload'


def test_token_expired(client):
    expired_token = jwt.encode({
        'user': 'admin',
        'role': 'admin',
        'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
    }, main.app.config['SECRET_KEY'], algorithm='HS256')

    resp = client.get('/protected', headers={'Authorization': f'Bearer {expired_token}'})
    assert resp.status_code == 401
    assert resp.get_json()['message'] == 'Token expired'


def test_role_denied(client):
    forbidden_token = jwt.encode({
        'user': 'admin',
        'role': 'guest',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, main.app.config['SECRET_KEY'], algorithm='HS256')

    resp = client.get('/protected', headers={'Authorization': f'Bearer {forbidden_token}'})
    assert resp.status_code == 403
    assert resp.get_json()['message'] == 'Access forbidden: Admins or users only'
