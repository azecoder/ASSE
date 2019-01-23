from flask import request
import json
from .serializable import Serializable

class UserDto(Serializable):

    is_active = True
    is_anonymous = False
    id = None
    password = None
    strava_token = None

    def __init__ (self, dict):
        self._authenticated = False
        if dict is not None:
            self._populate(dict)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        #checked = self.password == password
        checked = self.password == password
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id

    def toJson (self):
        # return jsonify(
        #     id = self.id
        #     email = self.email
        #     firstname = self.firstname
        #     lastname = self.lastname
        #     age = self.age
        #     weight = self.weight
        #     max_hr = self.max_hr
        #     rest_hr = self.rest_hr
        #     vo2max = self.vo2max
        #     is_active = self.is_active
        #     is_admin = self.is_admin
        #     is_anonymous = self.is_anonymous
        # )

        return json.dumps(self.__dict__)
