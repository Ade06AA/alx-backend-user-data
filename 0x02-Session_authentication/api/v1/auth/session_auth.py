#!/usr/bin/env python3
"""
module for authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from base64 import b64decode
from typing import List, TypeVar, Dict
import uuid


class SessionAuth(Auth):
    """
    Sesion authentication
    note: a REST api is not meant to have a session
    """
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create sesion
        """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.__class__.user_id_by_session_id[session_id] = user_id
        return session_id

    def destroy_session(self, request=None):
        """
        delete a session
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if self.__class__.user_id_by_session_id.get(session_id):
            del self.user_id_by_session_id[session_id]
            return True
        else:
            return False

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        return user id
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return self.__class__.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        get the curent user
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user
