#!/usr/bin/python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

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
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def add_user_1(self, *args):
        """instantiate new user add it to database
        """
        user_obj = self.init_user(args)
        if user_obj:
            self.__session.add(user_obj)
            self.commit()
        return self.__session.query(User).filter_by(email=user_obj.email)

    def commit(self):
        self.__session.commit()

    def init_user(*args):

        if len(args) == 2:
            return User(args[0], args[1])
        if len(args) == 3:
            return User(args[0], args[1], args[2])
        if len(args) == 4:
            return User(args[0], args[1], args[2], args[3])
        return None


if __name__ == "__main__":
    my_db = DB()

    user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    print(user_1.id)

    user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
    print(user_2.id)
