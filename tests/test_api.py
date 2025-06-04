import os
import pytest
import jwt

# Setup environment variables before importing the app
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('USERNAME', 'testuser')
os.environ.setdefault('PASSWORD', 'testpass')
os.environ.setdefault('ROLE', 'admin')

from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login_returns_token(client):
    resp = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'token' in data and data['token']

def test_protected_no_token(client):
    resp = client.get('/protected')
    assert resp.status_code == 401

def test_protected_with_valid_token(client):
    login_resp = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    token = login_resp.get_json()['token']
    resp = client.get('/protected', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
    assert resp.get_json().get('message') == 'Access granted'

def test_login_ignores_invalid_role(client):
    resp = client.post('/login', json={'username': 'testuser', 'password': 'testpass', 'role': 'invalid'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'token' in data
    decoded = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms=['HS256'])
    assert decoded['role'] == 'admin'
