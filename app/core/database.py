from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import ibm_db_dbi
from app.core.config import settings

def create_db2_connection():
    """
    Custom connection creator for IBM DB2 with SSL support
    """
    conn_string = (
        f"DATABASE={settings.DB2_DATABASE};"
        f"HOSTNAME={settings.DB2_HOSTNAME};"
        f"PORT={settings.DB2_PORT};"
        f"PROTOCOL={settings.DB2_PROTOCOL};"
        f"UID={settings.DB2_USERNAME};"
        f"PWD={settings.DB2_PASSWORD};"
        f"SECURITY={settings.DB2_SECURITY};"
    )
    
    return ibm_db_dbi.connect(conn_string, "", "")

# Create engine
engine = create_engine(
    "db2+ibm_db://",
    creator=create_db2_connection,
    pool_pre_ping=True,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
    pool_recycle=settings.SQLALCHEMY_POOL_RECYCLE,
    echo=settings.SQLALCHEMY_ECHO,
)

@event.listens_for(engine, "connect")
def set_db2_schema(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("SET CURRENT SCHEMA FSQ87086")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()