# JWT Auth API (Flask)

This is a simple REST API demonstrating JWT-based authentication using Flask.

## Features

- `/login`: Accepts username/password and returns a JWT token (valid for 30 minutes)
- `/protected`: Returns a success message only if valid JWT token is passed in `Authorization` header

## Usage

1. Start the server:
```bash
python main.py
```

2. Obtain a token:
```bash
curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{
  "username": "admin",
  "password": "123"
}'
```

3. Access the protected route with the token:
```bash
curl http://127.0.0.1:5000/protected -H "Authorization: Bearer <token>"
```
