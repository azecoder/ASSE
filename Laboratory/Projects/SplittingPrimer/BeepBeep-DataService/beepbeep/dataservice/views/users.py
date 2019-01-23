import os
from flakon import SwaggerBlueprint
from flask import request, jsonify
from beepbeep.dataservice.database import db, User, Run, Challenge, Objective
import requests

HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api-swagger.yaml')
users_api = SwaggerBlueprint('users', __name__, swagger_spec=YML)


def fill(source, target):
    for prop in source:
        setattr(target, prop, source[prop])


@users_api.operation('getUsers')
def get_users():
    users = db.session.query(User)
    return jsonify([user.to_json() for user in users])


@users_api.operation('createUser')
def create_user():
    raw_user = request.get_json()

    if raw_user is None:
        return "Invalid user body", 400

    user = User()
    fill(raw_user, user)

    exist_email = db.session.query(User).filter(
        User.email == user.email).count()
    if(exist_email > 0):
        return jsonify({"error": "A user with the same email already exists"}), 400

    try:
        db.session.add(user)
        db.session.commit()

        requests.post('http://127.0.0.1:5050/users',
                      json={
                          "id": user.id,
                          "email": user.email,
                          "password": user.password
                      })

    except Exception as e:  # pragma: no cover
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify(user.to_json()), 201


@users_api.operation('updateUserById')
def update_user_by_id(id):

    raw_user = request.get_json()

    if raw_user is None:
        return "Invalid user body", 400

    try:
        user = db.session.query(User).filter(User.id == id).first()

        if(user is None):
            return jsonify({"error": "User not found"}), 404

        fill(raw_user, user)
        db.session.commit()

        requests.put('http://127.0.0.1:5050/users',
                     json={
                         "id": user.id,
                         "email": user.email,
                         "password": user.password
                     })

    except Exception as e:  # pragma: no cover
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify(user.to_json()), 200


@users_api.operation('getUserById')
def get_user_by_id(id):
    try:
        user = db.session.query(User).filter(User.id == id).first()

        if(user is None):
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.to_json()), 200
    except Exception as e:  # pragma: no cover
        return jsonify({"error": str(e)}), 500


@users_api.operation('deleteUserById')
def delete_user_by_id(id):
    try:
        user = db.session.query(User).filter(User.id == id).first()
        if(user is None):
            return jsonify({"error": "User not found"}), 404

        requests.delete('http://127.0.0.1:5050/users',
                        json={
                            "id": user.id
                        })

        db.session.query(Run).filter(Run.runner_id == id).delete()
        db.session.query(Challenge).filter(Challenge.runner_id == id).delete()
        db.session.query(Objective).filter(Objective.user_id == id).delete()
        db.session.query(User).filter(User.id == id).delete()
        db.session.commit()

        return "", 204
    except Exception as e:  # pragma: no cover
        return jsonify({"error": str(e)}), 500
