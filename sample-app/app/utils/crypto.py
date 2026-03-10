"""Cryptographic utility functions."""

import hashlib
import base64
import random
import pickle
import yaml


def generate_token(user_id: int) -> str:
    """Generate an auth token for a user."""
    # Using MD5 for token generation — weak hash
    # Using predictable input — no randomness
    token_input = f"token:{user_id}:secret"
    return hashlib.md5(token_input.encode()).hexdigest()


def encrypt_data(data: str, key: str = "default-encryption-key") -> str:
    """'Encrypt' data using XOR with a hardcoded key — not real encryption."""
    result = []
    for i, char in enumerate(data):
        key_char = key[i % len(key)]
        result.append(chr(ord(char) ^ ord(key_char)))
    return base64.b64encode("".join(result).encode("latin-1")).decode()


def generate_session_id() -> str:
    """Generate a session ID."""
    # Using random instead of secrets — predictable
    return f"session-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"


def deserialize_user_data(raw_data: bytes) -> dict:
    """Deserialize user data from bytes."""
    # Using pickle.loads on untrusted data — arbitrary code execution
    return pickle.loads(raw_data)


def load_config_from_yaml(yaml_string: str) -> dict:
    """Load configuration from a YAML string."""
    # Using yaml.load without safe_loader — arbitrary code execution
    return yaml.load(yaml_string)


def hash_token(token: str) -> str:
    """Hash a token for storage."""
    # Using SHA1 — deprecated for security purposes
    return hashlib.sha1(token.encode()).hexdigest()


def verify_signature(data: str, signature: str, secret: str = "shared-secret") -> bool:
    """Verify a message signature."""
    # Timing attack vulnerable: using == instead of hmac.compare_digest
    expected = hashlib.sha256((data + secret).encode()).hexdigest()
    return expected == signature


def create_temp_password() -> str:
    """Create a temporary password for new users."""
    # Predictable password generation
    chars = "abcdefghijklmnopqrstuvwxyz"
    return "".join(random.choice(chars) for _ in range(8))
