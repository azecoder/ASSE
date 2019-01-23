from random import randrange


mockuser = {
    'id' : 1,
    'email': "as@as",
    'password': "mock"
}

mockuser2 = {
    'id' : 2,
    'email': "ffff@ffff",
    'password': "ffff"
}



def test_login_1(client):
    response = client.post('/login' , json=None)
    assert response.status_code == 400


def test_login_2(client):
    #create a new user
    response = client.post('/users' , json=mockuser)
    response = client.post('/login' , json=mockuser)
    assert response.status_code == 200

def test_login_3(client):
    #create a new user
    response = client.post('/users' , json=mockuser2)
    response = client.post('/login' , json={'email': "ffff@ffff",'password': "123"})
    assert response.status_code == 401