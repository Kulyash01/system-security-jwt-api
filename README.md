# JWT Auth API (Flask)

This example demonstrates a minimal REST API using Flask and JWT-based authentication.

## Features

- `/login`: Accepts a username and password, returning a short-lived JWT token.
- `/protected`: Example endpoint that validates a JWT token and requires the `admin` role.

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set required environment variables:

```bash
export SECRET_KEY="your-secret-key"
export USERNAME="admin"            # or use CREDENTIALS_FILE
export PASSWORD_HASH="<hashed password>"
# Optional: export CREDENTIALS_FILE=/path/to/credentials.json
# Optional: export FLASK_DEBUG=1   # enable Flask debug mode
```

The credentials file (if used) should contain JSON with `username` and `password_hash` fields.
If a plain `password` field is provided, it will be hashed on startup.

3. Run the application:

```bash
# Optional: enable debug output
export FLASK_DEBUG=1
python main.py
```

Send a login request and store the returned token:

```bash
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}' | jq -r '.token')
```

Use the token to call a protected endpoint:

```bash
curl http://localhost:5000/protected \
  -H "Authorization: Bearer $TOKEN"   # header will be: Authorization: Bearer <token>
```
