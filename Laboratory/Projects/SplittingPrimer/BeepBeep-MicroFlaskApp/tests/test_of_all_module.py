import json
from models.challenge import Challenge
from models.objective import Objective
from models.run import Run
from models.user import UserDto


##Test for challenge.py
def test_module_challenge():
    challenge = Challenge(None)
    assert challenge.toJson() == "{}"

    challenge = Challenge({
        "id": 1,
        "runner_id": 2,
        "run_id": 3,
        "latest_run_id": 4,
    })
    assert challenge.toJson() == '{"id": 1, "runner_id": 2, "run_id": 3, "latest_run_id": 4}'


##Test for objective.py
def test_module_objective():
    objective = Objective(None)
    assert objective.toJson() == {}

    objective = Objective({
        "objective_id": 1,
        "distance": 30,
        "user_id": 2,
    })
    assert objective.toJson() == {"objective_id": 1, "distance": 30, "user_id": 2}

##Test for run.py
def test_module_run():
    run = Run(None)
    assert run.toJson() == "{}"

    jsonstr = '{"id": 1, "title": "Run 1", "strava_id": 32, "distance": 1000, "start_date": 10102018, "elapsed_time": 1, "average_speed": 1, "average_heartrate": 60, "total_elevation_gain": 1, "runner_id": 1}'
    run = Run({
        "id": 1,
        "title": "Run 1",
        "strava_id": 32,
        "distance": 1000,
        "start_date": 10102018,
        "elapsed_time": 1,
        "average_speed": 1,
        "average_heartrate": 60,
        "total_elevation_gain": 1,
        "runner_id": 1,
    })
    assert run.toJson() == jsonstr

##Test for user.py
def test_module_user():

    user = UserDto({
        "id": 1,
        "email": "emal@em.it",
        "firstname": "gino",
        "lastname": "piripicchio",
        "age": 30,
        "weight": 70,
        "max_hr": 150,
        "rest_hr": 60,
        "vo2max": 10,
        "is_active": True,
        "is_admin": False,
        "is_anonymous": False
    })
    assert user.is_authenticated == False

