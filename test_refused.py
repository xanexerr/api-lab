import uuid


def test_duplicate_username_is_refused(api):
    user = {"username": "lab-" + uuid.uuid4().hex[:12], "password": "Pizza-2026"}
    first = api.post("/api/users", json=user)
    assert first.status_code == 201
    second = api.post("/api/users", json=user)
    assert second.status_code == 400
    assert second.json() == {"error": "username already taken"}


def test_wrong_password_is_refused(api):
    user = {"username": "lab-" + uuid.uuid4().hex[:12], "password": "Pizza-2026"}
    created = api.post("/api/users", json=user)
    assert created.status_code == 201
    wrong = {"username": user["username"], "password": "Wrong-Pizza-2026"}
    response = api.post("/api/users/token/login", json=wrong)
    assert response.status_code == 401
    assert response.json() == {"error": "authentication failed"}


def test_empty_username_is_refused(api):
    response = api.post(
        "/api/users",
        json={"username": "", "password": "Pizza-2026"},
    )
    assert response.status_code == 400
    assert response.json() == {"error": "username field is empty"}
