from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.skills import Skill
from app.schemas.skills import SkillCreate, SkillUpdate, SkillResponse
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[SkillResponse])
def get_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        items = db.query(Skill).offset(skip).limit(limit).all()
        if items is None:
            items = []
        return items
    except TypeError as e:
        print(f"DB2 TypeError in get_all skills: {e}")
        return []
    except Exception as e:
        print(f"Error fetching skills: {e}")
        return []

@router.get("/{item_id}", response_model=SkillResponse)
def get_one(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(Skill).filter(Skill.skill_id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Skill with ID {item_id} not found")
        return item
    except HTTPException:
        raise
    except TypeError as e:
        print(f"DB2 TypeError for skill {item_id}: {e}")
        raise HTTPException(status_code=404, detail=f"Skill with ID {item_id} not found")
    except Exception as e:
        print(f"Error fetching skill {item_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create(
    item: SkillCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        new_item = Skill(**item.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        print(f"Error creating skill: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating skill: {str(e)}")

@router.put("/{item_id}", response_model=SkillResponse)
def update(
    item_id: int,
    item_update: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(Skill).filter(Skill.skill_id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Skill with ID {item_id} not found")
        
        for key, value in item_update.dict(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item
    except HTTPException:
        raise
    except TypeError as e:
        print(f"DB2 TypeError updating skill {item_id}: {e}")
        raise HTTPException(status_code=404, detail=f"Skill with ID {item_id} not found")
    except Exception as e:
        db.rollback()
        print(f"Error updating skill {item_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating skill: {str(e)}")

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(Skill).filter(Skill.skill_id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Skill with ID {item_id} not found")
        
        db.delete(item)
        db.commit()
        return None
    except HTTPException:
        raise
    except TypeError as e:
        print(f"DB2 TypeError deleting skill {item_id}: {e}")
        raise HTTPException(status_code=404, detail=f"Skill with ID {item_id} not found")
    except Exception as e:
        db.rollback()
        print(f"Error deleting skill {item_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting skill: {str(e)}")
