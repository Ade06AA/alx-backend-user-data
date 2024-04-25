#!/usr/bin/env python3
"""
user ORM module
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String<F11>

Base = declarative_base()


class User(Base):
    """
    user database object
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,
                unique=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
