
PATH = "/users"

def test_create_objective(db, client):
    data = {
        "id": 1,
        "user_id": 1,
        "distance": 14
    }
    r = client.post( PATH + "/1/objectives", json=data )
    assert r.status_code == 200, "Should create an objective"


def test_get_objectives(db, client):
    r = client.get( PATH + "/1/objectives" )
    assert r.status_code == 200, "Should return the objectives"    
    objectives = r.get_json()
    assert len(objectives) == 1, "Should return an objective"

    assert list(objectives) == list([{
        "id": 1,
        "user_id": 1,
        "distance": 14        
    }]), "Should return the correct objective"

def test_get_objective_by_id(db, client):
    r = client.get( PATH + "/1/objectives/1" )   
    objective = r.get_json()
    assert r.status_code == 200, "Should return objective by id"
    assert dict(objective) == dict({
        "id": 1,
        "user_id": 1,
        "distance": 14        
    })

def test_get_inexistent_objective_by_id(db, client):
    r = client.get( PATH + "/1/objectives/21" )
    assert r.status_code == 404, "Should return 404"            

def test_update_objective(db, client):
    data = {
        "id": 1,
        "user_id": 1,
        "distance": 11          
    }
    r = client.put( PATH + "/1/objectives/1", json=data )
    assert r.status_code == 200

    objective = r.get_json()
    assert objective['distance'] == 11

def test_update_inexistent_objective(db, client):
    data = {
        "id": 1,
        "user_id": 56,
        "distance": 12        
    }
    r = client.put( PATH + "/1/objectives/16", json = data)
    assert r.status_code == 404, "Should return 404"

def test_update_invalid_json(db, client):
    r = client.put( PATH + "/1/objectives/1" )
    assert r.status_code == 400, "Invalid data, Should return 400"

def test_delete_objective_by_id(db, client):
    r = client.delete( PATH + "/1/objectives/1" )
    assert r.status_code == 204

def test_delete_inexsistent_objective_by_id(db, client):
    r = client.delete( PATH + "/1/objectives/45" )
    assert r.status_code == 404, "Should return 404"
