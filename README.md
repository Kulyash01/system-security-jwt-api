# JWT Auth API (Flask)

This example demonstrates a minimal REST API using Flask and JWT-based authentication.

## Features

- `/login`: Accepts a username and password, returning a short-lived JWT token.
- `/protected`: Example endpoint that validates a JWT token and requires the `admin` role.

## Usage

1. Set required environment variables:

```bash
export SECRET_KEY="your-secret-key"
export USERNAME="admin"            # or use CREDENTIALS_FILE
export PASSWORD_HASH="<hashed password>"
# Optional: export CREDENTIALS_FILE=/path/to/credentials.json
```

The credentials file (if used) should contain JSON with `username` and `password_hash` fields.
If a plain `password` field is provided, it will be hashed on startup.

2. Run the application:

```bash
python main.py
```

Send a login request:

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'
```

Use the returned token in the `Authorization` header when calling `/protected`.
