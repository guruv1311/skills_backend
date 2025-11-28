# Skills Management Backend API

FastAPI backend with **IBM AppID OAuth** (W3 SAML) authentication, SQLAlchemy ORM, and Alembic migrations.

## 🚀 Features

- 🔐 **IBM AppID OAuth/OIDC** authentication with W3 SAML integration
- 🔄 **Session-based** authentication (no JWT tokens needed)
- 📊 Complete database schema matching your requirements
- 🚀 Fast REST API with automatic OpenAPI documentation
- 🗄️ Database migrations with Alembic
- 🐬 MySQL/MariaDB support

## 📋 Prerequisites

- Python 3.8+
- MySQL or MariaDB database
- IBM AppID credentials (already configured in .env)

## 🛠️ Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Database

Update the `DATABASE_URL` in `.env`:

```env
DATABASE_URL=mysql+pymysql://your_user:your_password@localhost:3306/skills_db
```

Create the database:
```sql
CREATE DATABASE skills_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure Session Secret

Generate a strong session secret:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update `SESSION_SECRET` in `.env` with the generated value.

### 4. Initialize Database

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### 5. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 6. Access the Application

- 🌐 **API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc

## 🔑 Authentication Flow

### Login Process

1. **Navigate to**: `GET /auth/login`
2. **Redirected to**: IBM AppID login page (W3 SAML)
3. **After authentication**: Redirected to `/auth/auth/callback`
4. **Session created**: User info stored in server-side session
5. **Redirect to frontend**: `http://localhost:3000`

### Using Protected Endpoints

All API endpoints require an active session. The session cookie is automatically sent by the browser.

```bash
# Example: Get current user profile
curl -X GET http://localhost:8000/auth/user \
  --cookie "session=<session_cookie>"
```

### Logout

```bash
POST /auth/logout
```

Returns the W3 SAML logout URL and clears the session.

## 📡 API Endpoints

### Authentication Endpoints

- `GET /auth/login` - Initiate OAuth login
- `GET /auth/callback` - OAuth callback
- `GET /auth/user` - Get current user profile
- `POST /auth/logout` - Logout and clear session
- `GET /auth/validate` - Validate session
- `GET /auth/check` - Check authentication status

### Protected Resource Endpoints

All require active session:

- `/api/users` - User management
- `/api/skills` - Skills catalog
- `/api/projects` - Project management
- `/api/assets` - Asset management
- `/api/user-skills` - User skills
- `/api/user-cert` - Certifications
- `/api/requests` - Approval requests

## 🗄️ Database Schema

Tables matching your diagram:

- **users** - User accounts (populated from OAuth)
- **skills** - Master skills catalog
- **user_skills** - User skill proficiencies with approval workflow
- **projects** - Project information
- **assets** - User-created assets
- **user_cert** - User certifications
- **request** - Approval workflow with JSON data storage

## ⚙️ Configuration

### Environment Variables (`.env`)

```env
# Database
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/skills_db

# IBM AppID (Pre-configured)
IBM_CLIENT_ID=afd7310a-855b-4367-8d81-377dbc3d5762
IBM_TENANT_ID=60a6e85d-e695-4cff-a88a-88ad53cc01d4
IBM_CLIENT_SECRET=<your_secret>
IBM_OAUTH_SERVER_URL=https://au-syd.appid.cloud.ibm.com/oauth/v4/60a6e85d-e695-4cff-a88a-88ad53cc01d4
IBM_DISCOVERY_ENDPOINT=https://au-syd.appid.cloud.ibm.com/oauth/v4/60a6e85d-e695-4cff-a88a-88ad53cc01d4/.well-known/openid-configuration

# Session (CHANGE THIS!)
SESSION_SECRET=your-super-secret-key-change-this-in-production

# Frontend
FRONTEND_URL=http://localhost:3000

# W3 Logout
W3_SLO_URL=https://preprod.login.w3.ibm.com/idaas/mtfim/sps/idaas/logout
```

## 🔧 Database Migrations

```bash
# Create new migration after model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## 🧪 Testing Authentication

### Test Login Flow

1. Open browser: `http://localhost:8000/auth/login`
2. Login with your IBM W3 credentials
3. You'll be redirected to your frontend with an active session
4. Test API access: `http://localhost:8000/auth/user`

### Test API Endpoint

```python
import requests

# Start session
session = requests.Session()

# Login (will redirect through OAuth)
login_url = "http://localhost:8000/auth/login"
response = session.get(login_url, allow_redirects=True)

# After manual login in browser, use the session
response = session.get("http://localhost:8000/auth/user")
print(response.json())
```

## 📁 Project Structure

```
fastapi_skills_backend/
├── app/
│   ├── main.py                 # App entry + OAuth config
│   ├── api/routes/             # API endpoints
│   ├── auth/
│   │   ├── routes.py           # OAuth routes
│   │   └── dependencies.py     # Session auth
│   ├── core/
│   │   ├── config.py           # Settings
│   │   └── database.py         # DB connection
│   ├── models/                 # SQLAlchemy models
│   └── schemas/                # Pydantic schemas
├── alembic/                    # Database migrations
├── .env                        # Configuration
└── requirements.txt            # Dependencies
```

## 🚀 Production Deployment

### Security Checklist

- ✅ Generate strong `SESSION_SECRET`
- ✅ Set `https_only=True` in SessionMiddleware
- ✅ Use HTTPS for all endpoints
- ✅ Update `FRONTEND_URL` to production domain
- ✅ Configure proper CORS origins
- ✅ Use strong database password
- ✅ Enable database SSL connection
- ✅ Set up proper logging
- ✅ Configure rate limiting

### Example Production Run

```bash
# Using Gunicorn with Uvicorn workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Test MySQL connection
mysql -u your_user -p -h localhost skills_db

# Check DATABASE_URL format
DATABASE_URL=mysql+pymysql://user:password@host:port/database
```

### OAuth Authentication Issues

- **Redirect URI mismatch**: Ensure IBM AppID has `http://localhost:8000/auth/auth/callback` registered
- **Session not persisting**: Check if cookies are enabled in your browser
- **CORS issues**: Verify `FRONTEND_URL` in `.env` matches your frontend domain

### Session Issues

- **Session expires quickly**: Increase `max_age` in SessionMiddleware (app/main.py)
- **Session not working**: Ensure `SESSION_SECRET` is set and strong

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Authlib Documentation](https://docs.authlib.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [IBM App ID Documentation](https://cloud.ibm.com/docs/appid)

## 📝 License

Internal use only.

## 👥 Support

For issues or questions, contact your development team.
