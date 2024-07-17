"""
Module defining SQLAlchemy models for the application.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base

class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): Primary key identifier for the user.
        email (str): Unique email address of the user.
        hashed_password (str): Hashed password of the user.
        is_active (bool): Indicates if the user account is active.
        created_at (datetime): Timestamp of when the user account was created.
        updated_at (datetime): Timestamp of when the user account was last updated.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)

    def __repr__(self):
        return (
            f"<User(id={self.id}, email={self.email}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})>"
        )
