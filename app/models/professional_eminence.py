from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class ProfessionalEminence(Base):
    __tablename__ = "professional_eminence"
    __table_args__ = {'schema': 'FSQ87086'}
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    manager_id = Column(String(50), ForeignKey("FSQ87086.USERS.USER_ID"), nullable=True, index=True)
    user_id = Column(String(50), ForeignKey("FSQ87086.USERS.USER_ID"), nullable=False, index=True)
    
    # Fields
    url = Column(String(1000), nullable=True)
    eminence_type = Column(String(50), nullable=False, index=True)
    description = Column(String(200), nullable=True)
    scope = Column('SCOPE', String(20), nullable=False, index=True, quote=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="professional_eminences")
    manager = relationship("User", foreign_keys=[manager_id])
    
    def __repr__(self):
        return f"<ProfessionalEminence(id={self.id}, type={self.eminence_type}, employee={self.employee_id})>"
