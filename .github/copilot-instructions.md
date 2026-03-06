# Copilot Code Review Instructions

Give a confidence score for every code review suggestion 1-10.

## 🐍 Python Best Practices

### Type Hints

- All function signatures **must** include type annotations for parameters and return values.
- Use `str`, `int`, `bool`, `list[T]`, `dict[K, V]` (Python 3.10+ built-in generics) instead of `typing.List`, `typing.Dict`, etc.
- Use `X | None` instead of `Optional[X]`.
- Flag any new function missing type hints.

### Docstrings

- All public functions, classes, and modules **must** have docstrings.
- Use Google-style docstrings:
  ```python
  def example(name: str) -> str:
      """Greet human by name.

      Args:
          name: The human's name.

      Returns:
          A friendly greeting string.
      """
  ```
- Flag any new public function or class that is missing a docstring.

### Imports

- Follow the standard import order: **stdlib → third-party → local**.
- Use absolute imports (e.g., `from app.utils.helpers import hash_password`), not relative imports.
- Do not use wildcard imports (`from module import *`).
- Flag unused imports.

### Naming Conventions

- Use `snake_case` for functions, methods, and variables.
- Use `PascalCase` for class names.
- Use `UPPER_SNAKE_CASE` for constants.
- Boolean variables and functions should read naturally: `is_active`, `has_permission`, `can_edit`.

### Error Handling

- Never use bare `except:` — always catch specific exception types.
- Prefer explicit error messages in exceptions.
- Flask routes must return proper HTTP status codes and JSON error bodies (e.g., `{"error": "..."}` with a `4xx`/`5xx` status code).
- Avoid silencing exceptions unless there is a documented reason.

### Security

- **Never** store passwords in plain text. Always use a secure hashing algorithm (e.g., PBKDF2-HMAC-SHA256 with a random salt).
- Use `hmac.compare_digest()` for constant-time comparison — never use `==` to compare hashes or tokens.
- Do not hardcode secrets, API keys, or credentials. Use environment variables.
- Flag any use of `eval()`, `exec()`, or `pickle.loads()` on untrusted input.
- Validate and sanitize all user input before use.
- Flag SQL string concatenation or f-strings in queries — always use parameterized queries or the ORM.

### Flask & SQLAlchemy Patterns

- Use Flask Blueprints to organize routes — never define routes directly on the app object.
- Use `db.session.get(Model, id)` instead of the deprecated `Model.query.get(id)`.
- Always call `db.session.commit()` after mutations; never leave sessions in a dirty state.
- Return meaningful HTTP status codes: `201` for creation, `204` for deletion, `422` for validation errors, `409` for conflicts.
- Use `request.get_json(silent=True)` and check for `None` before accessing the body.

### Testing

- Every new route or utility function **must** have corresponding tests.
- Use `pytest` as the test framework.
- Use fixtures (via `conftest.py`) for shared setup like the Flask test client and database.
- Test both success and error/edge-case paths.
- Never assert on non-deterministic values (timestamps, random IDs) without allowing a tolerance.

### Code Style & Formatting

- Follow **PEP 8** guidelines for all Python code.
- Maximum line length is **88 characters** (Black formatter default).
- Use trailing commas in multi-line data structures and function calls.
- Prefer f-strings over `str.format()` or `%` formatting for readability.

### General

- Keep functions small and focused — each function should do one thing.
- Avoid mutable default arguments (e.g., `def foo(items=[])`). Use `None` and initialize inside the function.
- Use list/dict/set comprehensions where they improve clarity, but avoid nesting them more than one level deep.
- Prefer `pathlib.Path` over `os.path` for file system operations.
- Use `datetime.now(timezone.utc)` instead of `datetime.utcnow()` (which is deprecated in Python 3.12+).
