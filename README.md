# JWT Auth API (Flask)

This is a simple REST API demonstrating JWT-based authentication using Flask.

## Features

- `/login`: Accepts username/password and returns a JWT token (valid for 30 minutes)
- `/protected`: Returns a success message only if valid JWT token is passed in `Authorization` header

## Usage

1. Run:
```bash
python main.py{
  "username": "admin",
  "password": "123"
}

Authorization: <token>
