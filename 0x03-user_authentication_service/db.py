#!/usr/bin/python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import (Base, User)

# GLOBALS
# engine = create_engine('postgresql://user:password@localhost/mydatabase')
# SessionLocal = sessionmaker(bind=engine)
# session = SessionLocal()


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


if __name__ == "__main__":
    my_db = DB()

    user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    print(user_1.id)

    user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
    print(user_2.id)
