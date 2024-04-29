#!/usr/bin/env python3
"""
auithentication
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    return a password hash
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    generate id
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db: DB = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register user
        """
        user: User = None
        try:
            user: User = self._db.find_user_by(email=email)
        except NoResultFound:
            pass
        if user:
            raise ValueError(f"User {email} already exists")
        user: User = self._db.add_user(email, _hash_password(password))
        return user

    def valid_login(self, email: str, passwd: str) -> bool:
        """
        check for correct password
        """
        user: User = None
        try:
            user: User = self._db.find_user_by(email=email)
        except Exception as e:
            return False
        if user:
            return bcrypt.checkpw(passwd.encode('utf-8'),
                                  user.hashed_password)
        return False

    def create_session(self, email: str):
        """
        session
        """
        user: User = None
        try:
            user: User = self._db.find_user_by(email=email)
        except Exception as e:
            return False
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        session
        """
        user: User = None
        if session_id is None:
            return None
        user: User = self._db.find_user_by(session_id=session_id)
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        destroy session
        """
        self._db.update_user(user_id, session_id=None)
        return None
