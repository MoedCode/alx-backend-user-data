#!/usr/bin/env python3
""" User Class module """
from sqlalchemy import (
    Column, Integer, String
)
from sqlalchemy.ext.declarative import declarative_base
from hashlib import sha256
Base = declarative_base()


class User(Base):
    """ user class """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
    # def __init__(self, email, hashed_password, session_id=None, reset_token=None):
    #     self.email = email
    #     self.hashed_password = hashed_password
    #     if session_id:
    #         self.session_id = session_id
    #     if reset_token:
    #         self.reset_token = reset_token


if __name__ == "__main__":
    print(User.__tablename__)
    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))
