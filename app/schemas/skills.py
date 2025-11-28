from pydantic import BaseModel
from typing import Optional

class SkillBase(BaseModel):
    platform: str
    segment: str
    product_portfolio: str
    speciality_area: str

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    platform: Optional[str] = None
    segment: Optional[str] = None
    product_portfolio: Optional[str] = None
    speciality_area: Optional[str] = None

class SkillResponse(SkillBase):
    skill_id: int
    class Config:
        from_attributes = True
