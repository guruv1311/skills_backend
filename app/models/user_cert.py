from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserCert(Base):
    __tablename__ = "USER_CERT"
    __table_args__ = {'schema': 'FSQ87086'}
    
    id = Column("ID", Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column("USER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID", ondelete="CASCADE"))
    cert_type = Column("CERT_TYPE", String(100))
    cert_name = Column("CERT_NAME", String(255))
    cert_file_path = Column("CERT_FILE_PATH", String(512))
    manager_id = Column("MANAGER_ID", String(50), ForeignKey("FSQ87086.USERS.USER_ID", ondelete="SET NULL"))
    status = Column("STATUS", String(50))
    cert_cat = Column("CERT_CAT", String(100))
    issue_date = Column("ISSUE_DATE", Date)
    
    user = relationship("User", foreign_keys=[user_id], back_populates="user_certs")
    manager = relationship("User", foreign_keys=[manager_id])
