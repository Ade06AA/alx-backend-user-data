#!/usr/bin/env python3
"""
module for authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from base64 import b64decode
from typing import List, TypeVar


class BasicAuth(Auth):
    """
    doc
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Return None if authorization_header is None
		Return None if authorization_header is not a string
		Return None if authorization_header doesn’t start by Basic (with a space at the end)
		Otherwise, return the value after Basic (after the space)
		You can assume authorization_header contains only one Basic
        """
        if not authorization_header or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(maxsplit=1)[-1]


    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Return None if base64_authorization_header is None
        Return None if base64_authorization_header is not a string
        Return None if base64_authorization_header is not a valid Base64 - you can use try/except
        Otherwise, return the decoded value as UTF8 string - you can use decode('utf-8')
        """
        if not base64_authorization_header or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = b64decode(base64_authorization_header).decode('utf-8')
        except Exception as e:
            return None
        return decoded

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        This method must return 2 values
        Return None, None if decoded_base64_authorization_header is None
        Return None, None if decoded_base64_authorization_header is not a string
        Return None, None if decoded_base64_authorization_header doesn’t contain :
        Otherwise, return the user email and the user password - these 2 values must be separated by a :
        """
        if not decoded_base64_authorization_header or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        _list: List = decoded_base64_authorization_header.split(':',1)
        if len(_list) != 2:
            return None, None
        return (*_list,)


    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Return None if user_email is None or not a string
        Return None if user_pwd is None or not a string
        Return None if your database (file) doesn’t contain any User instance with email equal to user_email - you should use the class method search of the User to lookup the list of users based on their email. Don’t forget to test all cases: “what if there is no user in DB?”, etc.
        Return None if user_pwd is not the password of the User instance found - you must use the method is_valid_password of User
        Otherwise, return the User instance
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        user = User.search({"email": user_email})
        if len(user) != 0:
            if user[0].is_valid_password(user_pwd):
                return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        doc
        """
        authHeader = self.authorization_header(request)
        authHeader= self.extract_base64_authorization_header(authHeader)
        authHeader = self.decode_base64_authorization_header(authHeader)
        cridentials = self.extract_user_credentials(authHeader)
        user = self.user_object_from_credentials(*cridentials)
        return user

