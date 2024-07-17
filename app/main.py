"""
Main module defining endpoints for user management.
"""

from datetime import timedelta
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app import crud, models, schemas, auth
from app.database import get_session_local, engine
from app.config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    db: Session = Depends(get_session_local),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint to generate an access token for authentication.

    Args:
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_session_local).
        form_data (OAuth2PasswordRequestForm, optional): Form data containing username and password. 
            Defaults to Depends().

    Returns:
        dict: Access token details.
    """
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session_local)):
    """
    Endpoint to create a new user.

    Args:
        user (schemas.UserCreate): User creation data.
        db (Session, optional): SQLAlchemy database session. 
            Defaults to Depends(get_session_local).

    Returns:
        schemas.User: Created user details.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    """
    Endpoint to get current user details.

    Args:
        current_user (schemas.User, optional): Current authenticated user. 
            Defaults to Depends(auth.get_current_active_user).

    Returns:
        schemas.User: Current user details.
    """
    return current_user

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_session_local)):
    """
    Endpoint to fetch users.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to fetch. Defaults to 10.
        db (Session, optional): SQLAlchemy database session. 
            Defaults to Depends(get_session_local).

    Returns:
        List[schemas.User]: List of users.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(get_session_local),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    """
    Endpoint to update user details.

    Args:
        user_id (int): User ID to update.
        user_data (schemas.UserUpdate): Updated user data.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_session_local).
        current_user (schemas.User, optional): Current authenticated user. 
            Defaults to Depends(auth.get_current_active_user).

    Raises:
        HTTPException: If user is not found or user does not have permission.

    Returns:
        schemas.User: Updated user details.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this user")
    db_user = crud.update_user(db, user_id, user_data)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: int,
    db: Session = Depends(get_session_local),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    """
    Endpoint to delete a user.

    Args:
        user_id (int): User ID to delete.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_session_local).
        current_user (schemas.User, optional): Current authenticated user. 
            Defaults to Depends(auth.get_current_active_user).

    Raises:
        HTTPException: If user is not found or user does not have permission.

    Returns:
        schemas.User: Deleted user details.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this user")
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
