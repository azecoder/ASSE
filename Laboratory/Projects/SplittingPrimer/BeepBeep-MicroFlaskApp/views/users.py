from flask import Blueprint, redirect, render_template, request, jsonify
from forms import UserForm, DeleteForm
from flask_login import current_user, logout_user

from models.user import UserDto
from models.run import Run
import requests
import os
import json
from config import DATASERVICE


users = Blueprint('users', __name__)


@users.route('/users')
def _users():
    users = requests.get(DATASERVICE + '/users').json()
    return render_template("users.html", users=users)


@users.route('/create_user', methods=['POST', 'GET'])
def create_user():
    form = UserForm()
    error = ''
    status_code = 200
    if form.validate_on_submit():
        new_user = UserDto({})
        form.populate_obj(new_user)

        response = requests.post(DATASERVICE + '/users', json=new_user.__dict__)

        if(response.status_code == 201):
            #new_user.id = response.json()['id']
            #db.session.add(new_user)
            #db.session.commit()
            return redirect('/users')
        else:
            error = "Insert another email"
            status_code = 400

    return render_template('create_user.html', form=form, error=error), status_code


@users.route("/delete_user", methods=['POST', 'GET'])
def delete_user():
    form = DeleteForm()
    status_code = 200
    try:
        email = current_user.email
    except AttributeError:
        return redirect('/login')

    if form.validate_on_submit():
        # verify user password
        password = form.data['password']

        delete_response = requests.delete(DATASERVICE + '/users/' + str(current_user.id))

        if delete_response.status_code == 204:
            logout_user()
            # delete the user and all his data
            #_delete_user(user)
            return redirect('/users')
        else:
            status_code = 401

    return render_template('delete_user.html', form=form, user_email=email), status_code
