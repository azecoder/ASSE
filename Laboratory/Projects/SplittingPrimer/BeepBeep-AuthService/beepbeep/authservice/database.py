import os
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    password = db.Column(db.Unicode(128))

    def to_json(self, secure=False):
        res = {}
        for attr in ('id', 'email'):
            value = getattr(self, attr)
            if isinstance(value, Decimal):
                value = float(value)
            res[attr] = value
        return res