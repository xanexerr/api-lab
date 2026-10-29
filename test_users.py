def test_new_user_has_no_ratings(api, auth):
    response = api.get("/api/ratings", headers=auth)
    assert response.status_code == 200
    assert response.json() == {"ratings": []}
