import pytest
import os

import subprocess

MOCK_DATASERVICE = "https://mockdataservice.com"
os.environ['DATA_SERVICE'] = MOCK_DATASERVICE

from app import create_testing_app


@pytest.fixture
def app():
    #subprocess.call(["./key.sh"])
    _app = create_testing_app()
    yield _app

@pytest.fixture
def client(app):
    client = app.test_client()

    yield client