from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.manager_emp import ManagerEmp
from app.schemas.manager_emp import (
    ManagerEmpCreate,
    ManagerEmpUpdate,
    ManagerEmpResponse
)
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ManagerEmpResponse])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(ManagerEmp).offset(skip).limit(limit).all()
    return items

@router.get("/{manager_id}", response_model=List[ManagerEmpResponse])
def get_employees_under_manager(
    manager_id: str,
    db: Session = Depends(get_db)
):
    items = db.query(ManagerEmp).filter(
        ManagerEmp.manager_id == manager_id
    ).all()

    if not items:
        raise HTTPException(status_code=404, detail="No employees found for this manager.")

    return items

@router.post("/", response_model=ManagerEmpResponse, status_code=status.HTTP_201_CREATED)
def create(item: ManagerEmpCreate, db: Session = Depends(get_db)):
    new_item = ManagerEmp(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.put("/{manager_id}/{employee_id}", response_model=ManagerEmpResponse)
def update(manager_id: str, employee_id: str, item_update: ManagerEmpUpdate, db: Session = Depends(get_db)):
    item = db.query(ManagerEmp).filter(
        ManagerEmp.manager_id == manager_id,
        ManagerEmp.employee_id == employee_id
    ).first()

    if not item:
        raise HTTPException(404, "Manager-Employee relation not found")

    for key, value in item_update.dict(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{manager_id}/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(manager_id: str, employee_id: str, db: Session = Depends(get_db)):
    item = db.query(ManagerEmp).filter(
        ManagerEmp.manager_id == manager_id,
        ManagerEmp.employee_id == employee_id
    ).first()

    if not item:
        raise HTTPException(404, "Manager-Employee relation not found")

    db.delete(item)
    db.commit()
    return None
