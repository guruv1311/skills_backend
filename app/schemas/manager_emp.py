# app/schemas/manager_emp.py

from pydantic import BaseModel
from typing import Optional

class ManagerEmpBase(BaseModel):
    platform: Optional[str] = None
    segment: Optional[str] = None
    product_portfolio: Optional[str] = None
    speciality_area: Optional[str] = None

class ManagerEmpCreate(ManagerEmpBase):
    manager_id: str
    employee_id: str

class ManagerEmpUpdate(ManagerEmpBase):
    pass

class ManagerEmpResponse(ManagerEmpBase):
    manager_id: str
    employee_id: str

    class Config:
        orm_mode = True
