from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # IBM Cloud DB2 Configuration
    DB2_DATABASE: str = "bludb"
    DB2_HOSTNAME: str = "1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud"
    DB2_PORT: int = 32286
    DB2_USERNAME: str = "qfk97200"
    DB2_PASSWORD: str = "opn6MIJ6W3nuMjnH"
    DB2_PROTOCOL: str = "TCPIP"
    DB2_SECURITY: str = "SSL"

    # SQLAlchemy Configuration
    SQLALCHEMY_POOL_SIZE: int = 5
    SQLALCHEMY_MAX_OVERFLOW: int = 10
    SQLALCHEMY_POOL_TIMEOUT: int = 30
    SQLALCHEMY_POOL_RECYCLE: int = 3600
    SQLALCHEMY_ECHO: bool = False

    # IBM AppID OAuth Configuration
    IBM_CLIENT_ID: str
    IBM_TENANT_ID: str
    IBM_CLIENT_SECRET: str
    IBM_OAUTH_SERVER_URL: str
    IBM_PROFILES_URL: str
    IBM_DISCOVERY_ENDPOINT: str

    # Session Configuration
    SESSION_SECRET: str

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # W3 SAML Logout
    W3_SLO_URL: str = "https://preprod.login.w3.ibm.com/idaas/mtfim/sps/idaas/logout"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()