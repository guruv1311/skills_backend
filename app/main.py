from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from app.core.config import settings
from app.api.routes import users, skills, projects, assets, user_skills, user_cert, request, professional_eminence, team
from app.auth import routes as auth_routes
from app.api.routes import manager_emp


app = FastAPI(
    title="Skills Management API",
    description="API for managing user skills, projects, certifications, and assets with IBM AppID OAuth",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session Middleware (Required for OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET,
    max_age=3600,  # 1 hour session lifetime
    same_site="lax",
    https_only=False,  # Set to True in production with HTTPS
)

# OAuth Configuration for IBM AppID
oauth = OAuth()
oauth.register(
    name='appid',
    client_id=settings.IBM_CLIENT_ID,
    client_secret=settings.IBM_CLIENT_SECRET,
    server_metadata_url=settings.IBM_DISCOVERY_ENDPOINT,
    client_kwargs={
        'scope': 'openid email profile',
    }
)

# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(skills.router, prefix="/api/skills", tags=["skills"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(assets.router, prefix="/api/assets", tags=["assets"])
app.include_router(user_skills.router, prefix="/api/user-skills", tags=["user-skills"])
app.include_router(user_cert.router, prefix="/api/user-cert", tags=["user-certifications"])
app.include_router(request.router, prefix="/api/requests", tags=["requests"])
app.include_router(professional_eminence.router, prefix="/api/professional-eminence", tags=["professional-eminence"])
app.include_router(team.router, prefix="/api/team", tags=["team-management"])
app.include_router(manager_emp.router, prefix="/manager-emp", tags=["Manager-Employee Mapping"])

@app.get("/")
async def root():
    return {"message": "Skills Management API with IBM AppID OAuth", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",              # <file_name>:app
        host="0.0.0.0",
        port=8000,
        reload=True             # auto reload during development
    )