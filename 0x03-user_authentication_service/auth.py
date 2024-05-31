#!/usr/bin/env python3
from bcrypt import *
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union
from db import DB
from user import User


def _hash_password(password: str) -> str:
    """
    Returned bytes is a salted hash of the input password
    """
    return hashpw(password.encode(), gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Constructor method
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session
        """
        try:
            usr_id = self._db.find_user_by(email=email).id
            session_id = _generate_uuid()
            self._db.update_user(user_id=usr_id, session_id=session_id)
        except Exception:
            session_id = None
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get a user from a session ID
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Get a reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a user password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id, reset_token=None,
                                 hashed_password=_hash_password(password))
        except NoResultFound:
            raise ValueError
