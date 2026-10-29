import uuid

import pytest
import requests


SITE = "https://quickpizza.grafana.com"


class QuickPizza(requests.Session):
    def request(self, method, url, *args, **kwargs):
        if url.startswith("/"):
            url = SITE + url
        return super().request(method, url, *args, **kwargs)


@pytest.fixture(scope="session")
def api():
    session = QuickPizza()
    yield session
    session.close()


def log_in_new_user(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    created = api.post("/api/users", json=user)
    assert created.status_code == 201
    login = api.post("/api/users/token/login", json=user)
    assert login.status_code == 200
    return {"Authorization": "token " + login.json()["token"]}


@pytest.fixture
def auth(api):
    return log_in_new_user(api)


@pytest.fixture
def pizza_id(api, auth):
    response = api.post("/api/pizza", json={}, headers=auth)
    assert response.status_code == 200
    return response.json()["pizza"]["id"]


@pytest.fixture
def rating(api, auth, pizza_id):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        headers=auth,
    )
    assert response.status_code == 201
    made = response.json()
    yield made
    api.delete(f"/api/ratings/{made['id']}", headers=auth)


@pytest.fixture
def other_auth(api):
    return log_in_new_user(api)
