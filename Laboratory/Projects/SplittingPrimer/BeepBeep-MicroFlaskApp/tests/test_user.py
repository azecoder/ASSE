
from tests.user_context import *

email = "mock@example.com"
password = "7"

exampleuser = {
            'id': 22,
            'email': email,
            'firstname': 'Mario',
            'lastname': 'Rossi',
            'password': password,
            'strava_token' : 'f4k&t0ken',
            'age': '7',
            'weight': '22',
            'max_hr': '22',
            'rest_hr': '22',
            'vo2max': '7'
        }


def test_create_user(client, requests_mock ):
    response = UserContext.create_user(client, requests_mock, user_json=exampleuser)

    assert response.status_code == 200


def test_login_user(client, requests_mock):
    UserContext.create_user(client, requests_mock)
    response = UserContext.login(client)

    assert response.status_code == 200


def test_badlogin_user(client, requests_mock):
    UserContext.create_user(client,requests_mock)
    requests_mock.post(MOCK_AUTHSERVICE + '/login', status_code=401)
    response = UserContext.login(client, password="wrong")

    assert response.status_code == 401


def test_delete_user(client, requests_mock):
    create_login_user(client, requests_mock)

    response = UserContext.delete_user(client)
    assert response.status_code == 200


def test_baddelete_user(client, requests_mock):
    create_login_user(client, requests_mock)
    requests_mock.delete(MOCK_DATASERVICE + "/users/42", json="", status_code=401)
    response = UserContext.delete_user(client, password="wrong")

    assert response.status_code == 401