import pytest
import os
from beepbeep.authservice.app import create_app
from beepbeep.authservice.database import db as _db
import subprocess

from beepbeep.authservice.app import create_testing_app


@pytest.fixture(scope="module")
def app():
    #subprocess.call(["./key.sh"])
    _app = create_testing_app()
    yield _app
#     os.unlink('testdb.db')

@pytest.fixture(scope="module")
def db_instance(app):
    db.init_app(app)
    db.create_all(app=app)
    with app.app_context():
        yield db

@pytest.fixture(scope="module")
def client(app):
    client = app.test_client()
    yield client
