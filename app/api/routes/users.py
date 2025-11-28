from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from app.core.database import get_db
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate, UserResponse
from app.auth.dependencies import get_current_user
router = APIRouter()
@router.get("/", response_model=List[UserResponse])
def get_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        items = db.query(User).offset(skip).limit(limit).all()
        if items is None:
            items = []
        return items
    except TypeError as e:
        print(f"DB2 TypeError in get_all users: {e}")
        return []
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []
@router.get("/{item_id}", response_model=UserResponse)
def get_one(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(User).filter(User.user_id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"User with ID {item_id} not found")
        return item
    except HTTPException:
        raise
    except TypeError as e:
        print(f"DB2 TypeError for user_id {item_id}: {e}")
        raise HTTPException(status_code=404, detail=f"User with ID {item_id} not found")
    except Exception as e:
        print(f"Error fetching user {item_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create(
    item: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        print(f"DEBUG: create user payload: {item.dict()}")
        print("DEBUG: Checking for existing user by ID...")
        try:
            existing = db.query(User).filter(User.user_id == item.user_id).first()
        except TypeError:
            existing = None
        if not existing:
            print("DEBUG: Checking for existing user by Email...")
            try:
                existing = db.query(User).filter(User.email == item.email).first()
            except TypeError:
                existing = None
        print(f"DEBUG: Existing user check result: {existing}")
        if existing:
            print("DEBUG: User exists, returning existing user")
            return existing
        print("DEBUG: Creating new user instance...")
        user_data = item.dict()
        new_item = User(**user_data)
        print(f"DEBUG: New item created: {new_item}")
        print("DEBUG: Adding to DB...")
        db.add(new_item)
        print("DEBUG: Committing...")
        db.commit()
        print("DEBUG: Refreshing...")
        db.refresh(new_item)
        print("DEBUG: User created successfully")
        return new_item
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
@router.put("/{item_id}", response_model=UserResponse)
def update(
    item_id: str,
    item_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(User).filter(User.user_id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"User with ID {item_id} not found")
        for key, value in item_update.dict(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item
    except HTTPException:
        raise
    except TypeError as e:
        print(f"DB2 TypeError updating user {item_id}: {e}")
        raise HTTPException(status_code=404, detail=f"User with ID {item_id} not found")
    except Exception as e:
        db.rollback()
        print(f"Error updating user {item_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(User).filter(User.user_id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"User with ID {item_id} not found")
        db.delete(item)
        db.commit()
        return None
    except HTTPException:
        raise
    except TypeError as e:
        print(f"DB2 TypeError deleting user {item_id}: {e}")
        raise HTTPException(status_code=404, detail=f"User with ID {item_id} not found")
    except Exception as e:
        db.rollback()
        print(f"Error deleting user {item_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")