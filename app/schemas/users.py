from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str
    user_type: str
    
    manager_id: Optional[str] = None
    is_manager: Optional[bool] = False

class UserCreate(UserBase):
    user_id: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    user_type: Optional[str] = None
    
    manager_id: Optional[str] = None
    is_manager: Optional[bool] = None

class UserResponse(UserBase):
    user_id: str
    class Config:
        from_attributes = True
