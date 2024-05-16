#!/usr/bin/env python3
"""
Defines a hash_password function to return a hashed password
"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """
    Returns a encoded hashed password instance from  <class 'bytes'>
    Args:
        password (str): password to be hashed
    """
    b = password.encode()
    hashed = hashpw(b, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check  the password  validation
    Args:
        hashed_password (bytes):
        encoded hashed password instance from  <class 'bytes'>
        password (str): password in string
    Return:
        bool
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

if __name__ == "__main__":
    PWD  = "myPass"
    hasPWD = hash_password(PWD)
    print(f"hashed password : {hasPWD}")
    print(f"hashed password : {type(hasPWD)}")
    print(f"is password valid : {is_valid(hasPWD, PWD)} ")
    # print(f"is password valid {is_valid(hasPWD, PWD)} ")
