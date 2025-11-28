from pydantic import BaseModel
from typing import Optional

class AssetBase(BaseModel):
    user_id: str
    asset_name: str
    asset_desc: str
    used_in_project: Optional[str] = None
    ai_adoption: Optional[str] = None
    your_contribution: str
    manager_id: Optional[str] = None
    status: str = "pending"
    url: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    asset_name: Optional[str] = None
    status: Optional[str] = None

class AssetResponse(AssetBase):
    id: int
    class Config:
        from_attributes = True
