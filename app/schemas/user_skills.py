from pydantic import BaseModel
from typing import Optional
from datetime import date as DateType

class UserSkillBase(BaseModel):
    user_id: str
    proficiency_level: str
    platform: str
    segment: str
    product_portfolio: str
    speciality_area: str
    product_line: str
    manager_id: Optional[str] = None
    status: str = "pending"
    skill_type: str
    yoe: str
    date: Optional[DateType] = None

class UserSkillCreate(UserSkillBase):
    pass

class UserSkillUpdate(BaseModel):
    proficiency_level: Optional[str] = None
    status: Optional[str] = None

class UserSkillResponse(UserSkillBase):
    id: int
    class Config:
        from_attributes = True
