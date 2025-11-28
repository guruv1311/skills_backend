from fastapi import Request, HTTPException, status
from typing import Dict
import logging

logger = logging.getLogger(__name__)

async def get_current_user(request: Request) -> Dict:
    '''Dependency to get the current authenticated user from session'''
    user = request.session.get('user')
    
    if not user:
        logger.warning("Unauthenticated access attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract IBM user ID from nested structure
    user_id = None
    try:
        identities = user.get("identities", [])
        if identities and len(identities) > 0:
            idp_user_info = identities[0].get("idpUserInfo", {})
            attributes = idp_user_info.get("attributes", {})
            user_id = attributes.get("uid")
    except (KeyError, IndexError, AttributeError) as e:
        logger.error(f"Error extracting user_id from session: {e}")
    
    # Fallback to sub if uid not found
    if not user_id:
        user_id = user.get("sub")
    
    if not user_id:
        logger.error("User ID not found in session data")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in authentication data"
        )
    
    # Return normalized user data with user_id at top level
    normalized_user = {
        "user_id": user_id,  # IBM UID like '005SOZ744'
        "sub": user.get("sub"),
        "name": user.get("name"),
        "email": user.get("email"),
        "given_name": user.get("given_name"),
        "family_name": user.get("family_name"),
        "raw_user": user  # Keep original for reference
    }
    
    logger.info(f"User authenticated: {user_id} ({user.get('email')})")
    return normalized_user

async def get_current_user_optional(request: Request) -> Dict | None:
    '''Optional user from session - returns None if not authenticated'''
    user = request.session.get('user')
    
    if not user:
        return None
    
    # Extract and normalize user data same as get_current_user
    user_id = None
    try:
        identities = user.get("identities", [])
        if identities and len(identities) > 0:
            idp_user_info = identities[0].get("idpUserInfo", {})
            attributes = idp_user_info.get("attributes", {})
            user_id = attributes.get("uid")
    except (KeyError, IndexError, AttributeError):
        pass
    
    if not user_id:
        user_id = user.get("sub")
    
    if not user_id:
        return None
    
    return {
        "user_id": user_id,
        "sub": user.get("sub"),
        "name": user.get("name"),
        "email": user.get("email"),
        "given_name": user.get("given_name"),
        "family_name": user.get("family_name"),
        "raw_user": user
    }
