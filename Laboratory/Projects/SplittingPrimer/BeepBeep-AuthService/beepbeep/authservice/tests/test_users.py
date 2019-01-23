mockuser = {
    'id': 11,
    'email': "email@email",
    'password': "password"
}


def test_insert_user_auth(client):
    response = client.post('/users' , json=mockuser)
    assert response.status_code == 204


def test_update_user_auth(client):
    response = client.put('/users' , json=mockuser)
    assert response.status_code == 204


def test_delete_user_auth(client):
    response = client.delete('/users' , json=mockuser)
    assert response.status_code == 204