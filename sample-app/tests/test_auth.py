import json


def _register(client, username="carol", email="carol@example.com", password="mypassword"):
    return client.post(
        "/users/",
        data=json.dumps({"username": username, "email": email, "password": password}),
        content_type="application/json",
    )


def _login(client, username="carol", password="mypassword"):
    return client.post(
        "/auth/login",
        data=json.dumps({"username": username, "password": password}),
        content_type="application/json",
    )


class TestLogin:
    def test_successful_login(self, client):
        _register(client)
        resp = _login(client)
        assert resp.status_code == 200
        assert resp.get_json()["message"] == "Login successful"

    def test_wrong_password(self, client):
        _register(client)
        resp = _login(client, password="wrongpassword")
        assert resp.status_code == 401

    def test_unknown_user(self, client):
        resp = _login(client, username="nobody")
        assert resp.status_code == 401

    def test_missing_credentials(self, client):
        resp = client.post(
            "/auth/login",
            data=json.dumps({"username": "carol"}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_requires_json(self, client):
        resp = client.post("/auth/login", data="bad", content_type="text/plain")
        assert resp.status_code == 400

    def test_disabled_account(self, client):
        user_id = _register(client).get_json()["id"]
        client.put(
            f"/users/{user_id}",
            data=json.dumps({"is_active": False}),
            content_type="application/json",
        )
        resp = _login(client)
        assert resp.status_code == 403


class TestLogout:
    def test_logout(self, client):
        resp = client.post("/auth/logout")
        assert resp.status_code == 200
        assert resp.get_json()["message"] == "Logged out successfully"
