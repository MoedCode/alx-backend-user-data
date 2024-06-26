#!/usr/bin/env python3
"""basic auth module"""
from api.v1.auth.auth import Auth
import base64
from flask import request
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """basic auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 authorization header"""
        if authorization_header is None or\
            not isinstance(authorization_header, str) or\
                not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """decode base64 authorization header"""
        b_None = base64_authorization_header is None
        if b_None or not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                     decoded_base64_authorization_header:
                                     str) -> Tuple[str, str]:
            """Extracts the username and password
            from a decoded base64 authorization header.

            Args:
                decoded_base64_authorization_header (str):
                The decoded base64 authorization header.

            Returns:
                Tuple[str, str]:
                A tuple containing the username and password
                extracted from the header.
                    If the header is invalid or
                    missing, returns (None, None).
            """
            if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str) or\
                    ':' not in decoded_base64_authorization_header:
                return (None, None)
            return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self,
                                         user_email: str,
                                         user_pwd: str) -> TypeVar('User'):
            """
            Retrieve a user object based on the provided credentials.

            Args:
                user_email (str): The email of the user.
                user_pwd (str): The password of the user.

            Returns:
                User: The user object if
                the credentials are valid, None otherwise.
            """
            x = user_pwd is None or not isinstance(user_pwd, str)
            if user_email is None or not isinstance(user_email, str) or x:
                return None
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
            """Returns the current user based on the provided request.

            Args:
                request (Request): The request object (default: None).

            Returns:
                User: The current user object.

            """
            auth_header = self.authorization_header(request)
            if not auth_header:
                return None
            extract_base64 = self.extract_base64_authorization_header(auth_header)
            decode_base64 = self.decode_base64_authorization_header(extract_base64)
            user_credentials = self.extract_user_credentials(decode_base64)
            user_email = user_credentials[0]
            user_password = user_credentials[1]
            user_credentials = self.user_object_from_credentials(
                user_email, user_password)
            return user_credentials
