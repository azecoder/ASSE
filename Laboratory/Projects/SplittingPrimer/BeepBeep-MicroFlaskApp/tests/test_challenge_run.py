from tests.user_context import *
from pyquery import PyQuery as pq


def test_challenge_run(client, requests_mock):

    # generate some runs
    runs = []
    for i in ['1', '2', '3', '4', '5']:
        # creating 5 incrementally better runs, except for the fourth one which is bad
        run = {
            "id": i,
            "title": "Example Run"+str(i),
            "description": "Nice run "+str(i),
            "strava_id": 42,
            "runner_id": 42,
            "start_date": "2018112"+str(i),
            "average_heartrate": 22,
            "total_elevation_gain": 10,
        }
        d = {}
        if i != '4':
            d.update({
                "average_speed": float(i),
                "elapsed_time": float(i)*1000,
                "distance": 25 + float(i),
            })
        else:
            d.update({
                "average_speed": 0,
                "elapsed_time": 1,
                "distance": 1,
            })
        run.update(d)
        runs.append(run)

    with UserContext(client, requests_mock,runs_json=runs) as uc:
        data = {
            "id": 1,
            "run_id": 1,
            "runner_id": 42,
            "latest_run_id": 3
        }
        requests_mock.get(MOCK_DATASERVICE + "/users/42/challenges", json=[data], status_code=200)
        requests_mock.put(MOCK_DATASERVICE + "/users/42/challenges/1", json=data, status_code=200)
        requests_mock.get(MOCK_DATASERVICE + "/users/42/runs/getMaxId", json={"max_id": 5}, status_code=200)

        res = client.post("/challenge", data={"runs":[1]}, follow_redirects=True)
        
        html = pq(res.data)
        
        v = [i.attr("style") for i in html.items('.run')]
        
        assert v[data["run_id"]-1] == "color:yellow"


def test_request_more_than_challenge(client, requests_mock):

    with UserContext(client, requests_mock) as uc:
        res = client.post("/challenge", data={"run":[1,2]}, follow_redirects=True)

        html = pq(res.data)
        assert str.strip(html("#challengeError").html()) == "Please select exactly one run to challenge"

def test_request_challenge_no_logged(client, requests_mock):

    res = client.post("/challenge", data={"run":[1]}, follow_redirects=True)
        
    html = pq(res.data)
    assert html("#User").html() == "Hi, Anonymous"
    