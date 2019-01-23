from flakon import JsonBlueprint
from flask import request, jsonify
from beepbeep.authservice.database import db, User
from werkzeug.security import check_password_hash

login = JsonBlueprint('login', __name__)


@login.route('/login', methods=['POST'])
def _login():

    data = request.get_json()

    if data is not None:
        email = data['email']
        password = data['password']

        if email is not None and password is not None:
            user = db.session.query(User).filter(User.email == email).first()
            if(user is not None):
                if user.password == password:
                    return jsonify(user.to_json()), 200
                return "Bad credentials", 401

    return "", 400
