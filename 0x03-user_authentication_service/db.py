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

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update users attributes
        Returns: None
        """
        user = self.find_user_by(id=user_id)

        column_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_names:
                raise ValueError

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()


if __name__ == "__main__":
    my_db = DB()

    my_db = DB()

    email = 'test@test.com'
    hashed_password = "hashedPwd"

    user = my_db.add_user(email, hashed_password)
    print(user.id)

    try:
        my_db.update_user(user.id, hashed_password='NewPwd')
        print("Password updated")
    except ValueError:
        print("Error")
