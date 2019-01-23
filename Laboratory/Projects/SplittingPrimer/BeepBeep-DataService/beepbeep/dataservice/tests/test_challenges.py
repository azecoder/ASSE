
PATH = "/users"

def test_create_challange(db,client):
    data = {
        "id": 1,
        "run_id": 1,
        "latest_run_id": 0
    }
    r = client.post( PATH + "/1/challenges", json=data)
    data.update({"runner_id": 1})

    request = r.get_json()
    assert request == data

    r = client.get( PATH + "/1/challenges/1" )
    challenge = r.get_json()
    assert challenge == data

def test_create_challanges_invalid_user(db, client):
    data = {
        "id": 2,
        "run_id": 1,
        "latest_run_id": 0
    }
    r = client.post( PATH + "/66/challenges", json=data)
    assert r.status_code == 400

def test_create_challange_already_exist(db, client):
    data = {
        "id": 1,
        "run_id": 1,
        "latest_run_id": 0
    }
    r = client.post( PATH + "/1/challenges", json=data)
    assert r.status_code == 400

def test_get_challanges(db, client):
    r = client.get( PATH +  "/1/challenges").get_json()
    assert len(r) == 1

    assert list(r) == list([
    {
        "id": 1,
        "run_id": 1,
        "runner_id": 1,
        "latest_run_id": 0
    }])

def test_get_challange_by_id(db, client):
    r = client.get( PATH + "/1/challenges/1" )
    run = r.get_json()
    assert r.status_code == 200
    assert dict(run) == dict({
        "id": 1,
        "run_id": 1,
        "runner_id": 1,
        "latest_run_id": 0
    })

def test_get_inexistent_challange_by_id(db, client):
    r = client.get( PATH + "/1/challenges/8" )
    assert r.status_code == 404

def test_update_challange_by_id(db, client):
    data = {
        "id": 1,
        "run_id": 3,
        "latest_run_id": 0
    }
    r = client.put( PATH + "/1/challenges/1", json = data)
    challenge = r.get_json()
    data.update({"runner_id": 1})
    assert r.status_code == 200
    assert dict(challenge) == dict(data)

    r = client.get( PATH + "/1/challenges/1" )
    challenge = r.get_json()
    assert challenge == data


def test_update_inexistent_challange_by_id(db, client):
    data = {
        "id": 1,
        "run_id": 3,
        "latest_run_id": 0
    }
    r = client.put( PATH + "/1/challenges/8", json = data)
    assert r.status_code == 404

def test_update_invalid_json_challange_by_id(db, client):
    r = client.put( PATH + "/1/challenges/1")
    assert r.status_code == 400

def test_delete_challange_by_id(db, client):
    r = client.delete( PATH + "/1/challenges/1" )
    assert r.status_code == 204

def test_delete_inexistent_challange_by_id(db, client):
    r = client.delete( PATH + "/1/challenges/8" )
    assert r.status_code == 404