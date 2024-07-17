"""
Module responsible for CRUD operations on User entities in the database.
"""

from datetime import datetime
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.auth import get_password_hash

def get_user_by_email(db: Session, email: str) -> User:
    """
    Retrieve a user by their email address.

    Args:
        db (Session): SQLAlchemy database session.
        email (str): Email address of the user.

    Returns:
        User: User object if found, None otherwise.
    """
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int) -> User:
    """
    Retrieve a user by their ID.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user.

    Returns:
        User: User object if found, None otherwise.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    """
    Retrieve a list of users with optional pagination.

    Args:
        db (Session): SQLAlchemy database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to retrieve. Defaults to 10.

    Returns:
        list[User]: List of User objects.
    """
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db (Session): SQLAlchemy database session.
        user (UserCreate): UserCreate schema containing user data.

    Returns:
        User: Created User object.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, created_at=datetime.utcnow())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
    """
    Update an existing user in the database.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user to update.
        user_update (UserUpdate): UserUpdate schema containing updated user data.

    Returns:
        User: Updated User object if successful, None if user not found.
    """
    print("crud update start")
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    update_data = user_update.dict(exclude_unset=True)  # Exclude fields that are not updated
    if 'password' in update_data:
        update_data['hashed_password'] = get_password_hash(update_data.pop('password'))
    for key, value in update_data.items():
        setattr(db_user, key, value)
    print("crud update after minus")
    db_user.updated_at = datetime.utcnow()  # Set current time for updated_at
    print("crud update updated_at")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print("crud update end")
    return db_user

def delete_user(db: Session, user_id: int) -> User:
    """
    Delete a user from the database.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user to delete.

    Returns:
        User: Deleted User object if found and deleted, None if user not found.
    """
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
