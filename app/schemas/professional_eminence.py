from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

# Enums for dropdown values
class EminenceType(str, Enum):
    THOUGHT_LEADERSHIP = "Thought Leadership"
    SPEAKING_ENGAGEMENTS = "Speaking Engagements"
    AWARDS_RECOGNITIONS = "Awards & Recognitions"
    PATENTS_INNOVATIONS = "Patents / Innovations"
    COMMUNITY_CONTRIBUTIONS = "Community Contributions"

class Scope(str, Enum):
    IBM_INTERNAL = "IBM Internal"
    EXTERNAL = "External"
    BOTH = "Both"

# Base Schema
class ProfessionalEminenceBase(BaseModel):
    user_id: str = Field(..., max_length=50, description="Employee user ID")
    manager_id: Optional[str] = Field(None, max_length=50, description="Manager user ID")
    url: Optional[str] = Field(None, max_length=1000, description="URL to achievement")
    eminence_type: EminenceType = Field(..., description="Type of professional eminence")
    description: Optional[str] = Field(None, max_length=200, description="Brief summary (max 200 chars)")
    scope: Scope = Field(..., description="Scope of achievement")

# Create Schema (for POST requests)
class ProfessionalEminenceCreate(ProfessionalEminenceBase):
    pass

# Update Schema (for PUT/PATCH requests)
class ProfessionalEminenceUpdate(BaseModel):
    manager_id: Optional[str] = Field(None, max_length=50)
    url: Optional[str] = Field(None, max_length=1000)
    eminence_type: Optional[EminenceType] = None
    description: Optional[str] = Field(None, max_length=200)
    scope: Optional[Scope] = None

# Response Schema (for GET requests)
class ProfessionalEminenceResponse(BaseModel):
    id: int
    user_id: str
    manager_id: Optional[str] = None
    url: Optional[str] = None
    eminence_type: str
    description: Optional[str] = None
    scope: str
    
    class Config:
        from_attributes = True
