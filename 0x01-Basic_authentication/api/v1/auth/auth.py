#!/usr/bin/env python3
"""
module for authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        auth
        """
        if path is None or excluded_paths is None:
            return True
        path: str = path if path[-1] == '/' else path + '/'
        if path in excluded_paths:
            return False
        return True


    def authorization_header(self, request: request =None) ->  str:
        """
        auth
        """
        if request is None:
            return None
        if request.headers.get("Authorization") == None:
            return None
        return request.headers.get("Authorization")


    def current_user(self, request: request = None) -> TypeVar('User'):
        """
        auth
        """
        return None
