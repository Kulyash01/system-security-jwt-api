# JWT Auth API (Flask)

This example demonstrates a minimal REST API using Flask and JWT-based authentication.

## Features

- `/register`: Create a new user with a username, password and optional role.
- `/login`: Accepts a username and password and returns a short-lived JWT token using a predefined role.
- `/protected`: Example endpoint that validates a JWT token and requires either the `admin` or `user` role.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

For development or running the tests install the additional dependencies:

```bash
pip install -r requirements-dev.txt
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
export ROLE="admin"                # or use credentials file
# Optional: export CREDENTIALS_FILE=/path/to/credentials.json
# Optional: export FLASK_DEBUG=1   # enable Flask debug mode
```

The configured role is embedded into issued tokens. Any role value supplied in a
`/login` request is ignored.

If you use a credentials file, it should contain JSON with `username`, `password_hash`, and an optional `role` field. If a plain `password` field is provided, it will be hashed on startup.

Example credentials file:

```json
{
  "username": "admin",
  "password_hash": "<hashed password>",
  "role": "admin"
}
```

## Register

Create additional accounts using the `/register` endpoint. Provide a JSON body
with a `username`, `password` and optional `role` (defaults to `user`).

```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "newpass",
    "role": "user"
  }'
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

## Security, Performance, and Scalability

See [SECURITY.md](SECURITY.md) for guidelines on benchmarking the API, managing tokens, password hashing, and scaling the service.

## License

This project is licensed under the terms of the [MIT License](LICENSE).
