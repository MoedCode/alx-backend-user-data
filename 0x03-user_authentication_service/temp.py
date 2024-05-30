#!/usr/bin/env python3


import json
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine,
    Column, Integer, String
)
from sqlalchemy.orm import (
    sessionmaker, declarative_base
)
engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)

session = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}', fullname='{self.fullname}', nickname='{self.nickname}')>"


Base.metadata.create_all(engine)

val = [0x0f0cfac, "Mohamed", "ant mal omak", "ProCode"]

# Create a new User instance and set its attributes
user0 = User(id=val[0], name=val[1], fullname=val[2], nickname=val[3])

print(user0.__repr__())

# Add the user object to the session
session.add(user0)
# Commit the transaction to save the changes
session.commit()

# Fetch all users from the database
users = session.query(User).all()
print(users)

# def Fprintf(file_path="0-file", buffer=None, mode="a"):
#     with open(file_path, mode) as F:
#         if ".json" in file_path:
#             json.dump(buffer, F, indent=4)
#         else:
#             F.write(buffer)
