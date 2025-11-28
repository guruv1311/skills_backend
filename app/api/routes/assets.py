from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.assets import Asset
from app.schemas.assets import AssetCreate, AssetUpdate, AssetResponse
from app.auth.dependencies import get_current_user
router = APIRouter()
# @router.get("/", response_model=List[AssetResponse])
# def get_all(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     """Get all assets for the current authenticated user"""
#     try:
#         items = db.query(Asset).filter(
#             Asset.user_id == current_user.get("user_id")
#         ).offset(skip).limit(limit).all()
#         if items is None:
#             items = []
#         return items
#     except TypeError as e:
#         print(f"DB2 TypeError in get_all assets: {e}")
#         return []
#     except Exception as e:
#         print(f"Error fetching assets: {e}")
#         return []
@router.get("/{user_id}", response_model=List[AssetResponse])
def get_by_user(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all assets for a specific user"""
    try:
        items = db.query(Asset).filter(
            Asset.user_id == user_id
        ).offset(skip).limit(limit).all()
        if items is None:
            items = []
        return items
    except TypeError as e:
        print(f"DB2 TypeError fetching assets for user {user_id}: {e}")
        return []
    except Exception as e:
        print(f"Error fetching assets for user {user_id}: {e}")
        return []
@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create(
    item: AssetCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        asset_data = item.dict()
        asset_data['user_id'] = current_user["user_id"]
        new_item = Asset(**asset_data)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        print(f"Error creating asset: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating asset: {str(e)}")
@router.put("/{asset_id}", response_model=AssetResponse)
def update(
    asset_id: int,
    item_update: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(Asset).filter(
            Asset.id == asset_id
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Asset with ID {asset_id} not found")
        for key, value in item_update.dict(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error updating asset {asset_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating asset: {str(e)}")
@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        item = db.query(Asset).filter(
            Asset.id == asset_id,
            Asset.user_id == current_user["user_id"]
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Asset with ID {asset_id} not found")
        db.delete(item)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error deleting asset {asset_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting asset: {str(e)}")