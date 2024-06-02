#!/usr/bin/env python3
""" User Class module """
from sqlalchemy import (
    Column, Integer, String
)
from sqlalchemy.ext.declarative import declarative_base
from hashlib import sha256
Base = declarative_base()
import json

class User(Base):
    """ user class """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
    # def __dict__(self):
    #     printed = 0
    #     print('{', end="")
    #     for key in self:
    #         if printed:
    #             print(",", end="")
    #         print(f"{key} : {self.key}" , end="")
    #         printed = 1
    def to_dict(self):

        """Convert User object to dictionary"""
        return {
            'id': self.id  or None,
            'email': self.email,
            'hashed_password': self.hashed_password,
            'session_id': self.session_id or None,
            'reset_token': self.reset_token or None
        }
    def to_json(self):
        """Convert User object to JSON string"""
        return json.dumps(self.to_dict())



if __name__ == "__main__":
    print(User.__tablename__)
    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))
