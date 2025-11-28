# app/models/manager_emp.py

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ManagerEmp(Base):
    __tablename__ = "MANAGER_EMP"
    __table_args__ = {"schema": "FSQ87086"}

    manager_id = Column("MANAGER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID"), primary_key=True)
    employee_id = Column("EMPLOYEE_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID"), primary_key=True)

    platform = Column("PLATFORM", String(50))
    segment = Column("SEGMENT", String(50))
    product_portfolio = Column("PRODUCT_PORTFOLIO", String(50))
    speciality_area = Column("SPECIALITY_AREA", String(50))

    # relationships
    manager = relationship("User", foreign_keys=[manager_id], back_populates="employees")
    employee = relationship("User", foreign_keys=[employee_id], back_populates="managers")
