from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserSkill(Base):
    __tablename__ = "USER_SKILLS"
    __table_args__ = {'schema': 'FSQ87086'}
    
    id = Column("ID", Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column("USER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID", ondelete="CASCADE"))
    skill_id = Column("SKILL_ID", Integer, ForeignKey("FSQ87086.SKILLS.SKILL_ID", ondelete="CASCADE"))
    proficiency_level = Column("PROFICIENCY_LEVEL", String(50))
    platform = Column("PLATFORM", String(100))
    segment = Column("SEGMENT", String(100))
    product_portfolio = Column("PRODUCT_PORTFOLIO", String(100))
    speciality_area = Column("SPECIALITY_AREA", String(100))
    product_line = Column("PRODUCT_LINE", String(100))
    manager_id = Column("MANAGER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID", ondelete="SET NULL"))
    status = Column("STATUS", String(50))
    skill_type = Column("SKILL_TYPE", String(50))
    yoe = Column("YOE", String(50))
    date = Column("DATE", Date)
    
    user = relationship("User", foreign_keys=[user_id], back_populates="user_skills")
    manager = relationship("User", foreign_keys=[manager_id])
    skill = relationship("Skill", back_populates="user_skills")
