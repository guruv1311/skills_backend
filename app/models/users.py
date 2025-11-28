from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "USERS"
    __table_args__ = {'schema': 'FSQ87086'}
    
    user_id = Column("USER_ID", String(50), primary_key=True, index=True)
    user_type = Column("USER_TYPE", String(50))
    name = Column("NAME", String(255))
    email = Column("EMAIL", String(255), unique=True, index=True)
    
    user_skills = relationship("UserSkill", foreign_keys="UserSkill.user_id", back_populates="user", passive_deletes=True)
    projects = relationship("Project", foreign_keys="Project.user_id", back_populates="user", passive_deletes=True)
    user_certs = relationship("UserCert", foreign_keys="UserCert.user_id", back_populates="user", passive_deletes=True)
    assets = relationship("Asset", foreign_keys="Asset.user_id", back_populates="user", passive_deletes=True)
    managed_requests = relationship("Request", foreign_keys="Request.manager_id", back_populates="manager", passive_deletes=True)
    submitted_requests = relationship("Request", foreign_keys="Request.user_id", back_populates="user", passive_deletes=True)
    professional_eminences = relationship("ProfessionalEminence", foreign_keys="ProfessionalEminence.user_id", back_populates="user", passive_deletes=True)
    
    # NEW FIELDS
    manager_id = Column("MANAGER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID"), nullable=True)
    is_manager = Column("IS_MANAGER", Boolean, default=False)
    
    # Relations for manager hierarchy
    managers = relationship("ManagerEmp", foreign_keys="ManagerEmp.employee_id", back_populates="employee")
    employees = relationship("ManagerEmp", foreign_keys="ManagerEmp.manager_id", back_populates="manager")  