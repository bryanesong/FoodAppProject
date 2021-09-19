from typing import Iterable
from flask_main import db


class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = "food-app-users"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), index=False, unique=True, nullable=False)
    username = db.Column(db.String(64), index=False, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)

    def toDict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "username": self.username,
            "email": self.email,
            "created": self.created,
        }

    # def __dict__(self):
    #     return {
    #         "id": self.id,
    #         "uuid": self.uuid,
    #         "username": self.username,
    #         "email": self.email,
    #         "created": self.created,
    #     }

    def __repr__(self):
        return "<User {}>".format(self.username)

    # def __init__(self, uuid, username, email, created):
    #     self.uuid = uuid
    #     self.username = username
    #     self.email = email
    #     self.created = created
