def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    response = api.get(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert 400 <= response.status_code < 500
    owner_copy = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert owner_copy.status_code == 200
    assert owner_copy.json() == rating


def test_other_user_cannot_update_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    response = api.put(path, json={"stars": 5}, headers=other_auth)
    assert 400 <= response.status_code < 500
    owner_copy = api.get(path, headers=auth)
    assert owner_copy.status_code == 200
    assert owner_copy.json() == rating


def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    response = api.delete(path, headers=other_auth)
    assert 400 <= response.status_code < 500
    owner_copy = api.get(path, headers=auth)
    assert owner_copy.status_code == 200
    assert owner_copy.json() == rating
