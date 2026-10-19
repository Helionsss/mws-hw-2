import pytest

from api.config import API_PASSWORD, API_USERNAME
from api.rest_api import RestApi

INVALID_CREDENTIALS = [
    pytest.param(API_USERNAME, "wrong-password", id="wrong-password"),
    pytest.param("unknown-user", API_PASSWORD, id="unknown-user"),
]

INVALID_AUTH_HEADERS = [
    pytest.param({}, id="missing-token"),
    pytest.param({"Authorization": "Bearer invalid-token"}, id="invalid-token"),
    pytest.param({"Authorization": "Basic dXNlcjpwYXNz"}, id="wrong-auth-scheme"),
]


def test_login_token_identifies_the_same_user():
    api = RestApi()
    login_response = api.login()
    assert login_response.status_code == 200, login_response.text
    login_body = login_response.json()
    token = login_body.get("access_token")
    assert isinstance(token, str) and token.strip(), login_body

    me_response = api.get_me(token)
    assert me_response.status_code == 200, me_response.text
    profile = me_response.json()
    assert profile.get("id") == login_body.get("user", {}).get("id"), profile
    assert str(profile.get("username", "")).lower() == API_USERNAME.lower(), profile
    assert profile.get("email"), profile


@pytest.mark.parametrize("headers", INVALID_AUTH_HEADERS)
def test_profile_access_is_rejected_without_valid_token(headers):
    api = RestApi()
    response = api.get_me_with_headers(headers)
    assert response.status_code in (401, 403), response.text
    body = response.json()
    assert body.get("error") or body.get("message"), body


@pytest.mark.parametrize("username,password", INVALID_CREDENTIALS)
def test_login_rejects_invalid_credentials(username, password):
    api = RestApi()
    response = api.login(username, password)
    assert response.status_code in (400, 401), response.text
    body = response.json()
    assert body.get("error") or body.get("message"), body
