from pydantic import BaseModel
from typing import Optional
from datetime import date

class RequestCreate(BaseModel):
    manager_id: str
    user_id: str  # Add this field
    submission_date: date
    status: str
    request_data: Optional[str] = None  # Add this field
    section_type: str

class RequestUpdate(BaseModel):
    manager_id: Optional[str] = None
    user_id: Optional[str] = None
    submission_date: Optional[date] = None
    status: Optional[str] = None
    request_data: Optional[str] = None
    section_type: Optional[str] = None

class RequestResponse(BaseModel):
    request_id: int
    manager_id: str
    user_id: Optional[str] = None
    submission_date: date
    status: str
    request_data: Optional[str] = None
    section_type: str

    class Config:
        from_attributes = True
