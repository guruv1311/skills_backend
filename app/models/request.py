from sqlalchemy import Column, Integer, String, ForeignKey, Date, TEXT
from sqlalchemy.orm import relationship
from app.core.database import Base

class Request(Base):
    __tablename__ = "REQUEST"
    __table_args__ = {'schema': 'FSQ87086'}
    
    request_id = Column("REQUEST_ID", Integer, primary_key=True, index=True, autoincrement=True)
    manager_id = Column("MANAGER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID", ondelete="SET NULL"))
    user_id = Column("USER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID", ondelete="CASCADE"))
    submission_date = Column("SUBMISSION_DATE", Date)
    status = Column("STATUS", String(50))
    request_data = Column("REQUEST_DATA", TEXT)
    section_type = Column("SECTION_TYPE", String(50))
    
    manager = relationship("User", foreign_keys=[manager_id], back_populates="managed_requests")
    user = relationship("User", foreign_keys=[user_id], back_populates="submitted_requests")
