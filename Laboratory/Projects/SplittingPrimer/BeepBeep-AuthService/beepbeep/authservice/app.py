import os
from werkzeug.exceptions import HTTPException
from flakon import create_app as _create_app
from flakon.util import error_handling
from flask import request, abort, g, Flask
from flask_cors import CORS

import jwt

from .views import blueprints
from .database import db


_HERE = os.path.dirname(__file__)
os.environ['TESTDIR'] = os.path.join(_HERE, 'tests')
_SETTINGS = os.path.join(_HERE, 'settings.ini')


def create_app(settings=None):
    if settings is None:
        settings = _SETTINGS

    app = _create_app(blueprints=blueprints, settings=settings)

    with open(app.config['pub_key']) as f:
        app.config['pub_key'] = f.read()

    CORS(app)

    @app.before_request
    def before_req():
        if app.config.get('NEED_TOKEN', True):
            authenticate(app, request)

    return app


def _400(desc):
    exc = HTTPException()
    exc.code = 400
    exc.description = desc
    return error_handling(exc)


def authenticate(app, request):
    key = request.headers.get('Authorization')
    if key is None:
        return abort(401)

    key = key.split(' ')
    if len(key) != 2:
        return abort(401)

    if key[0].lower() != 'bearer':
        return abort(401)

    pub_key = app.config['pub_key']
    try:
        token = key[1]
        token = jwt.decode(token, pub_key, audience='beepbeep.io')
    except Exception as e:
        return abort(401)

    # we have the token ~ copied into the globals
    g.jwt_token = token

# used to create an app for testing
def create_testing_app():
    app = Flask(__name__)
    app.config['WTF_CSRF_SECRET_KEY'] = 'ec35ae128aa97f834ab848ecf823340875ddf483e9a535440cf68e05b3b38865'
    app.config['SECRET_KEY'] = '58c8f1ffb80e7d48d936cb8a485504498fc6c5dcfce18e3de6dcd3b851ff0540'
    app.config['STRAVA_CLIENT_ID'] = '00000'
    app.config['STRAVA_CLIENT_SECRET'] = '00000'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False # to mock rest services
    app.config['TESTING'] = True
    
    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.init_app(app)
    # login_manager.init_app(app)
    db.create_all(app=app)

    return app