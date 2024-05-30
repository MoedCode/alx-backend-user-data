#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import (Base, User)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """instantiate new user add it to database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        # print(f"user after instantiation  {new_user.__dict__}")
        self._session.add(new_user)
        self._session.commit()
        # print(f"user before return  {new_user.__dict__}")

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Return first row in users if keyword matches
        """
        if not kwargs:
            raise InvalidRequestError
        columns_list = User.__table__.columns.keys()

        for key in kwargs.keys():
            if key not in columns_list:
                raise InvalidRequestError
        user = self.__session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound

        return user


if __name__ == "__main__":
    my_db = DB()

    user = my_db.add_user("test@test.com", "PwdHashed")
    print(user.id)

    find_user = my_db.find_user_by(email="test@test.com")
    print(find_user.id)

    try:
        find_user = my_db.find_user_by(email="test2@test.com")
        print(find_user.id)
    except NoResultFound:
        print("Not found")

    try:
        find_user = my_db.find_user_by(no_email="test@test.com")
        print(find_user.id)
    except InvalidRequestError:
        print("Invalid")
