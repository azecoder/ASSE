from flask import Blueprint, render_template, redirect, request
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from stravalib import Client
from forms import LoginForm
import requests
from config import DATASERVICE
from models.user import UserDto

auth = Blueprint('auth', __name__)


def _populate(target, source):
    for prop in source:
        setattr(target, prop, source[prop])


@auth.route('/strava_auth')
@login_required
def _strava_auth():
    code = request.args.get('code')
    client = Client()
    xc = client.exchange_code_for_token
    access_token = xc(client_id=auth.app.config['STRAVA_CLIENT_ID'],
                      client_secret=auth.app.config['STRAVA_CLIENT_SECRET'],
                      code=code)
    current_user.strava_token = access_token

    user = requests.get(DATASERVICE + '/users/' + str(current_user.id)).json()
    user['strava_token'] = access_token
    requests.put(DATASERVICE + '/users/' + str(current_user.id), json=user).json()

    # db.session.add(current_user)
    # db.session.commit()

    print("is_authenticated " + str(current_user.is_authenticated))
    print("_authenticated " + str(current_user._authenticated))
    print("strava_token " + str(current_user.strava_token))

    return redirect('/')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = False
    status_code = 200
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        login_response = requests.post('http://127.0.0.1:5050/login', json={"email": email, "password": password})

        print("LOGIN STATUS CODE = " + str(login_response.status_code))
        
        if login_response.status_code == 200:

            user_from_as = login_response.json()
            user = requests.get(DATASERVICE + '/users/' + str(user_from_as['id'])).json()

            user_for_login = UserDto(user)
            user_for_login.password = password
            user_for_login.authenticate(password)

            print("USER => " + user_for_login.toJson())
            #_populate(user_for_login, user)

            login_user(user_for_login, force=True)
            return redirect('/')
        else:
            error = True
            status_code = 401

    return render_template('login.html',
                           form=form,
                           error=error,
                           current_user=current_user), status_code


@auth.route("/logout")
def logout():
    logout_user()
    return redirect('/')
