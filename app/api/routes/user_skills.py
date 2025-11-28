from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user_skills import UserSkill
from app.schemas.user_skills import UserSkillCreate, UserSkillUpdate, UserSkillResponse
from app.auth.dependencies import get_current_user
router = APIRouter()
# @router.get("/", response_model=List[UserSkillResponse])
# def get_all(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     """Get all skills for the current authenticated user"""
#     try:
#         items = db.query(UserSkill).filter(
#             UserSkill.user_id == current_user.get("user_id")
#         ).offset(skip).limit(limit).all()
#         if items is None:
#             items = []
#         return items
#     except Exception as e:
#         print("Error fetching user skills:", e)
#         return []
@router.get("/{user_id}", response_model=List[UserSkillResponse])
def get_by_user(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all skills for a specific user"""
    try:
        items = db.query(UserSkill).filter(
            UserSkill.user_id == user_id
        ).offset(skip).limit(limit).all()
        if items is None:
            items = []
        return items
    except Exception as e:
        print(f"Error fetching skills for user {user_id}:", e)
        return []
@router.post("/", response_model=UserSkillResponse, status_code=status.HTTP_201_CREATED)
def create(
    item: UserSkillCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        skill_data = item.dict()
        skill_data['user_id'] = current_user["user_id"]
        new_item = UserSkill(**skill_data)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        print(f"Error creating user skill: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating user skill: {str(e)}")
@router.put("/{skill_id}", response_model=UserSkillResponse)
def update(
    skill_id: int,
    item_update: UserSkillUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    item = db.query(UserSkill).filter(
        UserSkill.id == skill_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="User skill not found")
    for key, value in item_update.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item
@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    item = db.query(UserSkill).filter(
        UserSkill.id == skill_id,
        UserSkill.user_id == current_user["user_id"]
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="User skill not found")
    db.delete(item)
    db.commit()
    return None