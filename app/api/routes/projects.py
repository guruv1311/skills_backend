from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.projects import Project
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectResponse
from app.auth.dependencies import get_current_user

router = APIRouter()

# @router.get("/", response_model=List[ProjectResponse])
# def get_all(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     """Get all projects for the current authenticated user"""
#     try:
#         items = db.query(Project).filter(
#             Project.user_id == current_user.get("user_id")
#         ).offset(skip).limit(limit).all()
#         if items is None:
#             items = []
#         return items
#     except TypeError as e:
#         print(f"DB2 TypeError in get_all projects: {e}")
#         return []
#     except Exception as e:
#         print(f"Error fetching projects: {e}")
#         return []

@router.get("/{user_id}", response_model=List[ProjectResponse])
def get_by_user(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all projects for a specific user"""
    try:
        items = db.query(Project).filter(
            Project.user_id == user_id
        ).offset(skip).limit(limit).all()
        if items is None:
            items = []
        return items
    except TypeError as e:
        print(f"DB2 TypeError fetching projects for user {user_id}: {e}")
        return []
    except Exception as e:
        print(f"Error fetching projects for user {user_id}: {e}")
        return []

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create(
    item: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        project_data = item.dict()
        project_data['user_id'] = current_user["user_id"]
        new_item = Project(**project_data)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        print(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")

@router.put("/{project_id}", response_model=ProjectResponse)
def update(
    project_id: int,
    item_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(Project).filter(
            Project.id == project_id
            # Project.user_id == current_user["user_id"]
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
        
        for key, value in item_update.dict(exclude_unset=True).items():
            setattr(item, key, value)
        
        db.commit()
        db.refresh(item)
        return item
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error updating project {project_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating project: {str(e)}")

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == current_user["user_id"]
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
        
        db.delete(item)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error deleting project {project_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting project: {str(e)}")
