"""
Module defining Pydantic schemas for the application.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

def datetime_encoder(v):
    """
    Custom JSON encoder for datetime objects.
    
    Formats datetime objects as strings in '%Y-%m-%d %H:%M' format.
    Returns None for None values.
    """
    return v.strftime('%Y-%m-%d %H:%M') if v else None

# pylint: disable=too-few-public-methods
class UserBase(BaseModel):
    """
    Base schema for user data.

    Attributes:
        email (str): Email address of the user.
    """
    email: str

class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Attributes:
        password (str): Password for the new user.
    """
    password: str

class User(UserBase):
    """
    Detailed schema for user data, including database-specific fields.

    Attributes:
        id (int): Unique identifier for the user.
        is_active (bool): Indicates if the user account is active.
        created_at (datetime): Timestamp of when the user account was created.
        updated_at (Optional[datetime]): Timestamp of when the user account was last updated.
    """
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """
        Pydantic model configuration.

        Attributes:
            orm_mode (bool): Enable SQLAlchemy ORM mode for serialization/deserialization.
        """
        orm_mode = True
        json_encoders = {
            datetime: datetime_encoder
        }

class UserUpdate(BaseModel):
    """
    Schema for updating user data.

    Attributes:
        email (Optional[EmailStr]): Optional new email address for the user.
        password (Optional[str]): Optional new password for the user.
        is_active (Optional[bool]): Optional new active status for the user.
        updated_at (Optional[datetime]): Optional new timestamp for when the user was last updated.
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None
    updated_at: Optional[datetime] = None

    class Config:
        """
        Pydantic model configuration.

        Attributes:
            orm_mode (bool): Enable SQLAlchemy ORM mode for serialization/deserialization.
        """
        orm_mode = True
        json_encoders = {
            datetime: datetime_encoder
        }

class Token(BaseModel):
    """
    Schema for authentication token.

    Attributes:
        access_token (str): Access token string.
        token_type (str): Type of the token.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for token data.

    Attributes:
        email (Optional[str]): Optional email address associated with the token.
    """
    email: Optional[str] = None
