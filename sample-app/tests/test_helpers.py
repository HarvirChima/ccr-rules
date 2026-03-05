from app.utils.helpers import (
    hash_password,
    verify_password,
    is_valid_email,
    is_valid_username,
)


class TestPasswordHashing:
    def test_hash_is_not_plaintext(self):
        pw = "supersecret"
        hashed = hash_password(pw)
        assert pw not in hashed

    def test_verify_correct_password(self):
        pw = "supersecret"
        assert verify_password(pw, hash_password(pw)) is True

    def test_verify_wrong_password(self):
        assert verify_password("wrong", hash_password("correct")) is False

    def test_verify_bad_hash_format(self):
        assert verify_password("any", "notahash") is False

    def test_unique_salts(self):
        pw = "same"
        assert hash_password(pw) != hash_password(pw)


class TestEmailValidation:
    def test_valid_emails(self):
        for email in ("user@example.com", "a+b@x.co", "foo.bar@baz.org"):
            assert is_valid_email(email) is True

    def test_invalid_emails(self):
        for email in ("notanemail", "@example.com", "user@", "user@.com"):
            assert is_valid_email(email) is False


class TestUsernameValidation:
    def test_valid_usernames(self):
        for name in ("alice", "Bob_99", "user123"):
            assert is_valid_username(name) is True

    def test_invalid_usernames(self):
        for name in ("ab", "bad name", "has-hyphen", "x" * 81):
            assert is_valid_username(name) is False
