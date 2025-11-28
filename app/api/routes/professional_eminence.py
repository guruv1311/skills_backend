from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DatabaseError
from typing import List, Optional
from app.core.database import get_db
from app.models.professional_eminence import ProfessionalEminence
from app.models.users import User
from app.schemas.professional_eminence import (
    ProfessionalEminenceCreate,
    ProfessionalEminenceUpdate,
    ProfessionalEminenceResponse,
    EminenceType,
    Scope
)
from app.auth.dependencies import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def safe_query_all(query) -> List:
    """Safely execute query.all() handling DB2's None return"""
    try:
        results = query.all()
        if results is None:
            return []
        if not isinstance(results, list):
            return []
        return results
    except TypeError as e:
        logger.warning(f"TypeError in query execution (returning empty list): {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in query execution: {str(e)}")
        return []

# @router.get("/", response_model=List[ProfessionalEminenceResponse])
# def get_all_eminences(
#     skip: int = Query(0, ge=0),
#     limit: int = Query(100, ge=1, le=1000),
#     eminence_type: Optional[EminenceType] = None,
#     scope: Optional[Scope] = None,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     """Get all professional eminence records for the current authenticated user"""
#     try:
#         query = db.query(ProfessionalEminence).filter(
#             ProfessionalEminence.user_id == current_user.get("user_id")
#         )
        
#         if eminence_type:
#             query = query.filter(ProfessionalEminence.eminence_type == eminence_type)
#         if scope:
#             query = query.filter(ProfessionalEminence.scope == scope)
        
#         query = query.offset(skip).limit(limit)
#         items = safe_query_all(query)
#         return items
#     except DatabaseError as e:
#         logger.error(f"Database error in get_all_eminences: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Database error occurred"
#         )
#     except Exception as e:
#         logger.error(f"Unexpected error in get_all_eminences: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An unexpected error occurred"
#         )

@router.get("/{user_id}", response_model=List[ProfessionalEminenceResponse])
def get_by_user(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    eminence_type: Optional[EminenceType] = None,
    scope: Optional[Scope] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all professional eminence records for a specific user"""
    try:
        query = db.query(ProfessionalEminence).filter(
            ProfessionalEminence.user_id == user_id
        )
        
        if eminence_type:
            query = query.filter(ProfessionalEminence.eminence_type == eminence_type)
        if scope:
            query = query.filter(ProfessionalEminence.scope == scope)
        
        query = query.offset(skip).limit(limit)
        items = safe_query_all(query)
        return items
    except DatabaseError as e:
        logger.error(f"Database error fetching eminence for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(f"Unexpected error fetching eminence for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.post("/", response_model=ProfessionalEminenceResponse, status_code=status.HTTP_201_CREATED)
def create_eminence(
    eminence: ProfessionalEminenceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        eminence_data = eminence.dict()
        eminence_data['user_id'] = current_user["user_id"]
        
        user = db.query(User).filter(User.user_id == eminence_data['user_id']).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {eminence_data['user_id']} not found"
            )
        
        new_eminence = ProfessionalEminence(**eminence_data)
        db.add(new_eminence)
        db.commit()
        db.refresh(new_eminence)
        
        logger.info(f"Created professional eminence ID {new_eminence.id} for user {eminence_data['user_id']}")
        return new_eminence
        
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating eminence: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data: constraint violation"
        )
    except DatabaseError as e:
        db.rollback()
        logger.error(f"Database error creating eminence: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating eminence: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.put("/{eminence_id}", response_model=ProfessionalEminenceResponse)
def update_eminence(
    eminence_id: int,
    eminence_update: ProfessionalEminenceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        eminence = db.query(ProfessionalEminence).filter(
            ProfessionalEminence.id == eminence_id
            # ProfessionalEminence.user_id == current_user["user_id"]
        ).first()
        
        if not eminence:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Professional eminence with ID {eminence_id} not found"
            )
        
        update_data = eminence_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(eminence, key, value)
        
        db.commit()
        db.refresh(eminence)
        
        logger.info(f"Updated professional eminence ID {eminence_id}")
        return eminence
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating eminence {eminence_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.delete("/{eminence_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_eminence(
    eminence_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        eminence = db.query(ProfessionalEminence).filter(
            ProfessionalEminence.id == eminence_id,
            ProfessionalEminence.user_id == current_user["user_id"]
        ).first()
        
        if not eminence:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Professional eminence with ID {eminence_id} not found"
            )
        
        db.delete(eminence)
        db.commit()
        
        logger.info(f"Deleted professional eminence ID {eminence_id}")
        return None
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting eminence {eminence_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
