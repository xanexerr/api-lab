import requests

SITE = "https://quickpizza.grafana.com"
AUTH = {"Authorization": "token abcdef0123456789"}
VEGETARIAN = {"mustBeVegetarian": True}


def test_vegetarian_pizza():
    response = requests.post(SITE + "/api/pizza", json=VEGETARIAN, headers=AUTH)
    assert response.status_code == 200
    body = response.json()
    assert body["pizza"]["name"] != ""
    for ingredient in body["pizza"]["ingredients"]:
        assert ingredient["vegetarian"] is True, ingredient["name"]


def test_pizza_without_token_is_refused():
    response = requests.post(SITE + "/api/pizza", json=VEGETARIAN)
    assert response.status_code == 401
    assert response.json() == {"error": "authentication failed"}
