# ccr-rules – Sample Application

A simple Python/Flask REST API used as the **foundation for testing Copilot code-review rules**.

## Purpose

The app intentionally covers a broad set of coding patterns so that different code-review rules can be exercised against real, representative code:

| Area | What is covered |
|---|---|
| Input validation | username/email/password checks before persisting |
| Password security | PBKDF2-HMAC-SHA256 with per-password salt, constant-time compare |
| Error handling | 400 / 404 / 409 / 422 responses with descriptive JSON bodies |
| ORM / database | SQLAlchemy models, relationships, query pagination |
| Configuration | Environment-aware config classes (dev / test / prod) |
| Testing | pytest suite with fixtures, covering happy and error paths |

## Project Structure

```
sample-app/
├── app/
│   ├── __init__.py        # Application factory
│   ├── config.py          # Config classes per environment
│   ├── models.py          # SQLAlchemy models (User, Post)
│   ├── routes/
│   │   ├── auth.py        # POST /auth/login, /auth/logout
│   │   └── users.py       # CRUD /users/
│   └── utils/
│       └── helpers.py     # Password hashing, validation, pagination
├── tests/
│   ├── conftest.py        # Shared fixtures
│   ├── test_auth.py
│   ├── test_helpers.py
│   └── test_users.py
├── run.py                 # Development entry point
├── requirements.txt
└── requirements-dev.txt
```

## Quick Start

```bash
cd sample-app

# Install runtime dependencies
pip install -r requirements.txt

# Run the development server
python run.py
```

The API will be available at `http://127.0.0.1:5000`.

## Running the Tests

```bash
cd sample-app

# Install dev dependencies (includes pytest)
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=term-missing
```

## API Reference

### Users

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/users/` | List all users (paginated) |
| `POST` | `/users/` | Create a user |
| `GET` | `/users/<id>` | Get a user by ID |
| `PUT` | `/users/<id>` | Update a user |
| `DELETE` | `/users/<id>` | Delete a user |

### Auth

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/login` | Log in with username + password |
| `POST` | `/auth/logout` | Log out |

### Example – create a user

```bash
curl -X POST http://127.0.0.1:5000/users/ \
     -H "Content-Type: application/json" \
     -d '{"username":"alice","email":"alice@example.com","password":"hunter2!"}'
```

### Example – log in

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"alice","password":"hunter2!"}'
```
