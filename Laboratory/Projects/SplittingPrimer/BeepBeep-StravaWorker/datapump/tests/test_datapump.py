import unittest
import os
import json
import requests_mock
import requests

# Mock the DATA_SERVICE env variable before importing the datapump
testUrl = "https://test.com"
os.environ['DATA_SERVICE'] = testUrl

import datapump.datapump as dp


def test_push_to_dataservice(requests_mock):
    # Create a mock result
    runs = [
        {
            "average_heartrate": "null",
            "average_speed": 2.381,
            "description": "null",
            "distance": 1000.0,
            "elapsed_time": 420,
            "id": 4,
            "runner_id": 1,
            "start_date": 1541929800.0,
            "strava_id": 1958170800,
            "title": "Last Morning Walk",
            "total_elevation_gain": 5.0
        }
    ]
    # Register the fake call
    requests_mock.post(testUrl + "/users/1/runs", text=json.dumps(runs))

    # Make the call using the mock
    result = dp.push_to_dataservice(1,[]).text

    # Parse the result
    objResult = json.loads(result)

   # Assert valid call and response
    assert objResult[0]['start_date'] == 1541929800.0

def test_fetch_all_runs(requests_mock):

    requests_mock.post(testUrl + "/users/1/runs", json={})
    requests_mock.post(testUrl + "/users/2/runs", json={})
    requests_mock.get("https://www.strava.com/api/v3/athlete/activities?page=1&per_page=200&access_token=584949", json={})

    requests_mock.get(testUrl + "/users", json=[{"id": 1, 'strava_token': None, 'email': "em@k.it"}, {"id":2, 'strava_token': "584949", 'email': "em@k.it"}])
    dp.fetch_all_runs()
