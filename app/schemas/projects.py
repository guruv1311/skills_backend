from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    user_id: str
    project_name: str
    client_name: str
    tech_used: str
    your_role: str
    project_desc: str
    is_foak: bool = False
    asset_used: Optional[str] = None
    asset_name: Optional[str] = None
    manager_id: Optional[str] = None
    status: str = "pending"

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    status: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    class Config:
        from_attributes = True
