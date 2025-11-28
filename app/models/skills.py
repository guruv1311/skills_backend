from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Skill(Base):
    __tablename__ = "SKILLS"
    __table_args__ = {'schema': 'FSQ87086'}
    skill_id = Column("SKILL_ID", Integer, primary_key=True, index=True, autoincrement=True)
    platform = Column("PLATFORM", String(100))
    segment = Column("SEGMENT", String(100))
    product_portfolio = Column("PRODUCT_PORTFOLIO", String(100))
    speciality_area = Column("SPECIALITY_AREA", String(100))
    user_skills = relationship("UserSkill", back_populates="skill", passive_deletes=True)