#!/usr/bin/env python3
"""session auth module"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""
    def __init__(self) -> None:
        """Constructor method"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0
    
    def create_session(self, user_id=None):
        """Creates a session"""
        