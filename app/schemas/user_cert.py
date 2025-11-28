from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserCertBase(BaseModel):
    user_id: str
    cert_type: str
    cert_name: str
    cert_file_path: str
    manager_id: Optional[str] = None
    status: str = "pending"
    cert_cat: str
    issue_date: Optional[date] = None

class UserCertCreate(UserCertBase):
    pass

class UserCertUpdate(BaseModel):
    status: Optional[str] = None

class UserCertResponse(UserCertBase):
    id: int
    class Config:
        from_attributes = True
