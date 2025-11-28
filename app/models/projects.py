from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Project(Base):
    __tablename__ = "PROJECTS"
    __table_args__ = {'schema': 'FSQ87086'}
    
    id = Column("ID", Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column("USER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID", ondelete="CASCADE"))
    project_name = Column("PROJECT_NAME", String(255))
    client_name = Column("CLIENT_NAME", String(255))
    tech_used = Column("TECH_USED", Text)
    your_role = Column("YOUR_ROLE", String(255))
    project_desc = Column("PROJECT_DESC", Text)
    is_foak = Column("IS_FOAK", Boolean, default=False)
    asset_used = Column("ASSET_USED", String(255))
    asset_name = Column("ASSET_NAME", String(255))
    manager_id = Column("MANAGER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID", ondelete="SET NULL"))
    status = Column("STATUS", String(50))
    
    user = relationship("User", foreign_keys=[user_id], back_populates="projects")
    manager = relationship("User", foreign_keys=[manager_id])
