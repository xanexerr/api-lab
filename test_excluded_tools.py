import pytest


@pytest.mark.parametrize(
    "excluded",
    [[], ["Knife"], ["Scissors"], ["Knife", "Scissors"]],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    response = api.post("/api/pizza", json={"excludedTools": excluded}, headers=auth)
    assert response.status_code == 200
    assert response.json()["pizza"]["tool"] not in excluded


@pytest.mark.xfail(
    reason="Defect 1: excluding all tools causes a 500 response with an empty body",
    strict=True,
)
def test_excluding_all_tools_returns_client_error(api, auth):
    response = api.post(
        "/api/pizza",
        json={"excludedTools": ["Knife", "Pizza cutter", "Scissors"]},
        headers=auth,
    )
    assert response.status_code == 400
    assert response.json().get("error")
