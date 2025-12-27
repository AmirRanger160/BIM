from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserUpdate, UserResponse, PasswordChange
from app.core.security import require_admin, hash_password, verify_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserResponse], dependencies=[Depends(require_admin)])
async def get_users(db: Session = Depends(get_db)):
    """Get all users (admin only)."""
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users


@router.post("", response_model=UserResponse, dependencies=[Depends(require_admin)])
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user (admin only)."""
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exists"
        )

    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_admin=False,  # Default to non-admin, admin can change later
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_admin)])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update a user (admin only)."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = user_data.dict(exclude_unset=True)

    # Check for duplicate username/email if being updated
    if 'username' in update_data and update_data['username'] != db_user.username:
        existing = db.query(User).filter(
            User.username == update_data['username'],
            User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

    if 'email' in update_data and update_data['email'] != db_user.email:
        existing = db.query(User).filter(
            User.email == update_data['email'],
            User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a user (admin only)."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(db_user)
    db.commit()

    return None


@router.put("/{user_id}/password", response_model=UserResponse, dependencies=[Depends(require_admin)])
async def change_user_password(
    user_id: int,
    password_data: PasswordChange,
    db: Session = Depends(get_db)
):
    """Change a user's password (admin only)."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Verify old password
    if not verify_password(password_data.old_password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect"
        )

    # Update password
    db_user.hashed_password = hash_password(password_data.new_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
