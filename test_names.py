import requests


SITE = "https://quickpizza.grafana.com"


def test_names_are_listed():
    response = requests.get(SITE + "/api/names")
    assert response.status_code == 200
    assert "Margherita" in response.json()["names"]
