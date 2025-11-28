from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user_cert import UserCert
from app.schemas.user_cert import UserCertCreate, UserCertUpdate, UserCertResponse
from app.auth.dependencies import get_current_user

router = APIRouter()

# @router.get("/", response_model=List[UserCertResponse])
# def get_all(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     """Get all certifications for the current authenticated user"""
#     try:
#         items = db.query(UserCert).filter(
#             UserCert.user_id == current_user.get("user_id")
#         ).offset(skip).limit(limit).all()
#         if items is None:
#             items = []
#         return items
#     except TypeError as e:
#         print(f"DB2 TypeError in get_all user_certs: {e}")
#         return []
#     except Exception as e:
#         print(f"Error fetching user certs: {e}")
#         return []

@router.get("/{user_id}", response_model=List[UserCertResponse])
def get_by_user(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all certifications for a specific user"""
    try:
        items = db.query(UserCert).filter(
            UserCert.user_id == user_id
        ).offset(skip).limit(limit).all()
        if items is None:
            items = []
        return items
    except TypeError as e:
        print(f"DB2 TypeError fetching certs for user {user_id}: {e}")
        return []
    except Exception as e:
        print(f"Error fetching certs for user {user_id}: {e}")
        return []

@router.post("/", response_model=UserCertResponse, status_code=status.HTTP_201_CREATED)
def create(
    item: UserCertCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        cert_data = item.dict()
        cert_data['user_id'] = current_user["user_id"]
        new_item = UserCert(**cert_data)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        print(f"Error creating user cert: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating user cert: {str(e)}")

@router.put("/{cert_id}", response_model=UserCertResponse)
def update(
    cert_id: int,
    item_update: UserCertUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(UserCert).filter(
            UserCert.id == cert_id
            # UserCert.user_id == current_user["user_id"]
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Certificate with ID {cert_id} not found")
        
        for key, value in item_update.dict(exclude_unset=True).items():
            setattr(item, key, value)
        
        db.commit()
        db.refresh(item)
        return item
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error updating cert {cert_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating cert: {str(e)}")

@router.delete("/{cert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    cert_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(UserCert).filter(
            UserCert.id == cert_id,
            UserCert.user_id == current_user["user_id"]
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Certificate with ID {cert_id} not found")
        
        db.delete(item)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error deleting cert {cert_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting cert: {str(e)}")
