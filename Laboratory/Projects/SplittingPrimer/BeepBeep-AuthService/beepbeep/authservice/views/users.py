from flakon import JsonBlueprint
from flask import request
from beepbeep.authservice.database import db, User
import requests
import flask


users = JsonBlueprint('users', __name__)

# app = flask.Flask(__name__)


@users.route('/users', methods=['POST', 'PUT', 'DELETE'])
def _users():
    if request.method == 'POST':
        data = request.get_json()
        user = User()
        user.id = data['id']
        user.email = data['email']
        user.password = data['password']
        db.session.add(user) 
        db.session.commit()
        return "" , 204

    if request.method == 'PUT':
        data = request.get_json()
        user = db.session.query(User).filter(User.id == data['id']).first()
        if user is not None:
            user.email = data['email']
            user.password = data['password']
            db.session.commit()
            return "" , 204
        else:
            return "" , 404
       
    if request.method == 'DELETE':
        data = request.get_json()
        user = db.session.query(User).filter(User.id == data['id']).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return "" , 204
        else:
            return "" , 404
        

    return "",400