from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.request import Request
from app.schemas.request import RequestCreate, RequestUpdate, RequestResponse
from app.auth.dependencies import get_current_user

router = APIRouter()

# @router.get("/", response_model=List[RequestResponse])
# def get_all(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     """Get all requests for the current authenticated user"""
#     try:
#         items = db.query(Request).filter(
#             Request.user_id == current_user.get("user_id")
#         ).offset(skip).limit(limit).all()
#         if items is None:
#             items = []
#         return items
#     except TypeError as e:
#         print(f"DB2 TypeError in get_all requests: {e}")
#         return []
#     except Exception as e:
#         print(f"Error fetching requests: {e}")
#         return []

@router.get("/{user_id}", response_model=List[RequestResponse])
def get_by_user(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all requests for a specific user"""
    try:
        items = db.query(Request).filter(
            Request.manager_id == user_id,
            Request.status == "pending"
        ).offset(skip).limit(limit).all()
        if items is None:
            items = []
        return items
    except TypeError as e:
        print(f"DB2 TypeError fetching requests for user {user_id}: {e}")
        return []
    except Exception as e:
        print(f"Error fetching requests for user {user_id}: {e}")
        return []

@router.post("/", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
def create(
    item: RequestCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        request_data = item.dict()
        request_data['user_id'] = current_user["user_id"]
        new_item = Request(**request_data)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        print(f"Error creating request: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating request: {str(e)}")

@router.put("/{request_id}", response_model=RequestResponse)
def update(
    request_id: int,
    item_update: RequestUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(Request).filter(
            Request.request_id == request_id,
            Request.user_id == current_user["user_id"]
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Request with ID {request_id} not found")
        
        update_data = item_update.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(item, key, value)
        
        db.commit()
        db.refresh(item)
        return item
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error updating request {request_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating request: {str(e)}")

@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(Request).filter(
            Request.request_id == request_id,
            Request.user_id == current_user["user_id"]
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Request with ID {request_id} not found")
        
        db.delete(item)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error deleting request {request_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting request: {str(e)}")
