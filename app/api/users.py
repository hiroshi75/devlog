"""
User API endpoints
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.db.database import get_db
from app.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user"""
    # Check if user already exists
    if crud_user.get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    if crud_user.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    db_user = crud_user.create_user(db=db, user=user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    return db_user


@router.get("/", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    username: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all users with optional filters"""
    users = crud_user.get_users(
        db,
        skip=skip,
        limit=limit,
        username=username,
        email=email
    )
    return users


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific user by ID"""
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user 