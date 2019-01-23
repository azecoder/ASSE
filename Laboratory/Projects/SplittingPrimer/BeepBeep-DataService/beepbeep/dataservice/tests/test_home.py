

def test_home(db, client):
    r = client.get("/")
    json = r.get_json()

    assert json['here'] == 1

