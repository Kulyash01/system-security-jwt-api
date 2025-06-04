# JWT Auth API (Flask)

This example demonstrates a minimal REST API using Flask and JWT-based authentication.

## Features

- `/login`: Accepts a username and password, returning a short-lived JWT token.
- `/protected`: Example endpoint that validates a JWT token and requires either the `admin` or `user` role.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. (Optional) run the tests:

```bash
pytest
```

3. Set required environment variables:

```bash
export SECRET_KEY="your-secret-key"
export USERNAME="admin"            # or use CREDENTIALS_FILE
export PASSWORD_HASH="<hashed password>"
# Optional: export CREDENTIALS_FILE=/path/to/credentials.json
# Optional: export FLASK_DEBUG=1   # enable Flask debug mode
```

If you use a credentials file, it should contain JSON with `username` and `password_hash` fields. If a plain `password` field is provided, it will be hashed on startup.

Example credentials file:

```json
{
  "username": "admin",
  "password_hash": "<hashed password>"
}
```

## Usage

1. Start the server:

```bash
python main.py
```

2. Obtain a token:

```bash
curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{
  "username": "admin",
  "password": "your-password"
}'
```

3. Access the protected route with the token:

```bash
curl http://127.0.0.1:5000/protected -H "Authorization: Bearer <token>"
```

Alternatively, store the token in a variable:

```bash
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}' | jq -r '.token')
curl http://localhost:5000/protected -H "Authorization: Bearer $TOKEN"
```

Example raw HTTP request:

```http
GET /protected HTTP/1.1
Host: localhost:5000
Authorization: Bearer <token>
```

## License

This project is licensed under the terms of the [MIT License](LICENSE).
