from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Asset(Base):
    __tablename__ = "ASSETS"
    __table_args__ = {'schema': 'FSQ87086'}
    
    id = Column("ID", Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column("USER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID", ondelete="CASCADE"))
    asset_name = Column("ASSET_NAME", String(255))
    asset_desc = Column("ASSET_DESC", Text)
    used_in_project = Column("USED_IN_PROJECT", String(255))
    ai_adoption = Column("AI_ADOPTION", String(100))
    your_contribution = Column("YOUR_CONTRIBUTION", Text)
    manager_id = Column("MANAGER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID", ondelete="SET NULL"))
    status = Column("STATUS", String(50))
    url = Column("URL", String(512))
    
    user = relationship("User", foreign_keys=[user_id], back_populates="assets")
    manager = relationship("User", foreign_keys=[manager_id])
