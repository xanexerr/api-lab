import pytest


STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


def test_base_choice_is_saved(api, auth, pizza_id):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        headers=auth,
    )
    assert response.status_code == 201
    assert response.json()["stars"] == 3
    assert response.json()["pizza_id"] == pizza_id


@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": stars},
        headers=auth,
    )
    assert response.status_code == 400
    assert response.json() == {"error": STARS_ERROR}


@pytest.mark.parametrize(
    ("stars", "expected_status", "expected_body"),
    [
        (3.5, 400, {"error": "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"}),
        ("3", 400, {"error": "json: cannot unmarshal string into Go struct field Rating.stars of type int"}),
        (None, 400, {"error": STARS_ERROR}),
    ],
)
def test_stars_type_blocks(api, auth, pizza_id, stars, expected_status, expected_body):
    body = {"pizza_id": pizza_id}
    if stars is not None:
        body["stars"] = stars
    response = api.post("/api/ratings", json=body, headers=auth)
    assert response.status_code == expected_status
    assert response.json() == expected_body


def test_nonexistent_pizza_is_refused(api, auth):
    response = api.post(
        "/api/ratings",
        json={"pizza_id": 999999999, "stars": 3},
        headers=auth,
    )
    assert response.status_code == 400
    assert response.json() == {"error": "pizza ID 999999999 not found"}


def test_missing_token_is_refused(api, pizza_id):
    response = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3})
    assert response.status_code == 401
    assert response.json() == {"error": "authentication failed"}


@pytest.mark.xfail(
    reason="Defect 2: a made-up token can read the shared ratings list",
    strict=True,
)
def test_made_up_token_cannot_read_ratings(api):
    response = api.get(
        "/api/ratings",
        headers={"Authorization": "token 0000000000000000"},
    )
    assert response.status_code == 401
