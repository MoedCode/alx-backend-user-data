#!/usr/bin/env python3
from bcrypt import *


def _hash_password(password: str) -> str:
    """
    Returned bytes is a salted hash of the input password
    """
    return hashpw(password.encode(), gensalt())
