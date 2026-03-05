import json


def _create_user(client, username="alice", email="alice@example.com", password="secret123"):
    return client.post(
        "/users/",
        data=json.dumps({"username": username, "email": email, "password": password}),
        content_type="application/json",
    )


class TestListUsers:
    def test_empty_list(self, client):
        resp = client.get("/users/")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["users"] == []
        assert data["total"] == 0

    def test_list_after_create(self, client):
        _create_user(client)
        resp = client.get("/users/")
        assert resp.status_code == 200
        assert resp.get_json()["total"] == 1


class TestGetUser:
    def test_get_existing_user(self, client):
        create_resp = _create_user(client)
        user_id = create_resp.get_json()["id"]
        resp = client.get(f"/users/{user_id}")
        assert resp.status_code == 200
        assert resp.get_json()["username"] == "alice"

    def test_get_nonexistent_user(self, client):
        resp = client.get("/users/999")
        assert resp.status_code == 404


class TestCreateUser:
    def test_create_valid_user(self, client):
        resp = _create_user(client)
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["username"] == "alice"
        assert data["email"] == "alice@example.com"
        assert "password_hash" not in data

    def test_create_requires_json(self, client):
        resp = client.post("/users/", data="not json", content_type="text/plain")
        assert resp.status_code == 400

    def test_create_invalid_username(self, client):
        resp = _create_user(client, username="a!")
        assert resp.status_code == 422

    def test_create_invalid_email(self, client):
        resp = _create_user(client, email="not-an-email")
        assert resp.status_code == 422

    def test_create_short_password(self, client):
        resp = _create_user(client, password="short")
        assert resp.status_code == 422

    def test_create_duplicate_username(self, client):
        _create_user(client)
        resp = _create_user(client, email="other@example.com")
        assert resp.status_code == 409

    def test_create_duplicate_email(self, client):
        _create_user(client)
        resp = _create_user(client, username="bob")
        assert resp.status_code == 409


class TestUpdateUser:
    def test_update_email(self, client):
        user_id = _create_user(client).get_json()["id"]
        resp = client.put(
            f"/users/{user_id}",
            data=json.dumps({"email": "new@example.com"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.get_json()["email"] == "new@example.com"

    def test_update_nonexistent_user(self, client):
        resp = client.put(
            "/users/999",
            data=json.dumps({"email": "x@example.com"}),
            content_type="application/json",
        )
        assert resp.status_code == 404

    def test_update_requires_json(self, client):
        user_id = _create_user(client).get_json()["id"]
        resp = client.put(f"/users/{user_id}", data="bad", content_type="text/plain")
        assert resp.status_code == 400

    def test_update_invalid_email(self, client):
        user_id = _create_user(client).get_json()["id"]
        resp = client.put(
            f"/users/{user_id}",
            data=json.dumps({"email": "bad"}),
            content_type="application/json",
        )
        assert resp.status_code == 422

    def test_update_deactivate(self, client):
        user_id = _create_user(client).get_json()["id"]
        resp = client.put(
            f"/users/{user_id}",
            data=json.dumps({"is_active": False}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.get_json()["is_active"] is False


class TestDeleteUser:
    def test_delete_existing_user(self, client):
        user_id = _create_user(client).get_json()["id"]
        resp = client.delete(f"/users/{user_id}")
        assert resp.status_code == 204
        assert client.get(f"/users/{user_id}").status_code == 404

    def test_delete_nonexistent_user(self, client):
        resp = client.delete("/users/999")
        assert resp.status_code == 404
