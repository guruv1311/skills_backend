from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Dict
import logging
from authlib.integrations.base_client.errors import MismatchingStateError, OAuthError
from app.core.config import settings
from app.auth.dependencies import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/login")
async def login(request: Request):
    '''Start the OAuth/OIDC authorization code flow'''
    try:
        # CRITICAL: Clear any existing OAuth state before new login
        # This prevents state mismatch on subsequent logins
        keys_to_remove = [key for key in request.session.keys() if key.startswith('_')]
        for key in keys_to_remove:
            del request.session[key]
        
        # Also clear any existing auth state
        if '_state_appid_' in str(request.session.keys()):
            for key in list(request.session.keys()):
                if 'state' in key.lower() or 'appid' in key.lower():
                    del request.session[key]
        
        redirect_uri = str(request.url_for('auth_callback'))
        logger.info(f"Starting login flow with redirect_uri: {redirect_uri}")

        from app.main import oauth
        return await oauth.appid.authorize_redirect(request, redirect_uri)
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.get("/callback")
async def auth_callback(request: Request):
    '''OAuth callback endpoint'''
    try:
        logger.info("Processing auth callback")
        logger.debug(f"Session keys before token exchange: {list(request.session.keys())}")

        from app.main import oauth

        try:
            token = await oauth.appid.authorize_access_token(request)
        except MismatchingStateError as e:
            logger.warning(f"State mismatch detected, redirecting to login: {e}")
            # Clear the session and redirect to login
            request.session.clear()
            return RedirectResponse(url="/auth/login", status_code=302)
        except OAuthError as e:
            logger.error(f"OAuth error: {e}")
            request.session.clear()
            return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=oauth_error", status_code=302)

        logger.info("Token exchange successful")

        # Get user info
        try:
            user = await oauth.appid.parse_id_token(request, token)
            logger.info("ID token parsed successfully")
        except Exception as e:
            logger.warning(f"Failed to parse ID token, using userinfo endpoint: {e}")
            user = await oauth.appid.userinfo(token=token)

        # Clear OAuth state after successful authentication
        keys_to_remove = [key for key in request.session.keys() if key.startswith('_')]
        for key in keys_to_remove:
            del request.session[key]

        # Store user info in session
        request.session['user'] = {
            'sub': user.get('sub'),
            'name': user.get('name') or f"{user.get('given_name', '')} {user.get('family_name', '')}".strip(),
            'email': user.get('email'),
            'given_name': user.get('given_name'),
            'family_name': user.get('family_name'),
            'identities': user.get('identities'),
        }

        request.session['token'] = {
            'access_token': token.get('access_token'),
            'token_type': token.get('token_type'),
            'expires_at': token.get('expires_at'),
        }

        logger.info(f"User logged in: {user.get('email')}")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}")

    except MismatchingStateError:
        logger.warning("State mismatch - redirecting to login")
        request.session.clear()
        return RedirectResponse(url="/auth/login", status_code=302)
    except Exception as e:
        logger.error(f"Auth callback error: {e}", exc_info=True)
        request.session.clear()
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=auth_failed", status_code=302)


@router.get("/user")
async def get_user_profile(request: Request):
    '''Get current logged-in user profile'''
    user = request.session.get('user')
    token = request.session.get('token')
    if not user:
        return JSONResponse(status_code=401, content={'error': 'Not authenticated'})
    
    response_data = {'user': user}
    if token and 'access_token' in token:
        response_data['access_token'] = token['access_token']
        
    return response_data


@router.post("/logout")
@router.get("/logout")  # Also allow GET for easier testing
async def logout(request: Request):
    '''Logout user'''
    try:
        request.session.clear()
        
        response = JSONResponse(content={
            "message": "Logged out successfully",
            "logout_url": settings.W3_SLO_URL if hasattr(settings, 'W3_SLO_URL') else None,
        })
        
        # Clear session cookie
        response.delete_cookie(key="session", path="/")
        
        logger.info("User logged out, session cleared.")
        return response
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return JSONResponse(status_code=500, content={"message": f"Logout failed: {str(e)}"})


@router.get("/validate")
async def validate_session(current_user: Dict = Depends(get_current_user)):
    '''Validate if user session is active'''
    return {'valid': True, 'user': current_user}


@router.get("/check")
async def check_auth(request: Request):
    '''Check authentication status'''
    user = request.session.get('user')
    return {
        'authenticated': bool(user),
        'user': user if user else None
    }
