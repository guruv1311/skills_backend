import httpx
import logging
from typing import List, Optional, Dict
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class W3ProfileService:
    """Service to interact with IBM W3 Unified Profile API"""
    
    BASE_URL = "https://w3-unified-profile-api.ibm.com/v3/profiles"
    TIMEOUT = 30.0  # seconds
    
    @staticmethod
    async def get_user_profile(user_id: str) -> Optional[Dict]:
        """
        Fetch user profile from W3 API
        
        Args:
            user_id: User ID or email
            
        Returns:
            User profile data or None if not found
        """
        url = f"{W3ProfileService.BASE_URL}/{user_id}/profile_combined"
        
        try:
            async with httpx.AsyncClient(timeout=W3ProfileService.TIMEOUT) as client:
                response = await client.get(url)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    logger.warning(f"User {user_id} not found in W3 API")
                    return None
                else:
                    logger.error(f"W3 API error for user {user_id}: {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error(f"Timeout fetching profile for user {user_id}")
            raise HTTPException(status_code=504, detail="External API timeout")
        except Exception as e:
            logger.error(f"Error fetching W3 profile for {user_id}: {str(e)}")
            return None
    
    @staticmethod
    def extract_reportees(profile_data: Dict) -> List[str]:
        """
        Extract reportee user IDs from W3 profile data
        
        Args:
            profile_data: Full profile response from W3 API
            
        Returns:
            List of reportee user IDs
        """
        try:
            team_info = profile_data.get("content", {}).get("team_info", {})
            content = team_info.get("content", {})
            
            # Get functional reports (direct reports)
            functional_reports = content.get("functional", {}).get("reports", [])
            
            # Alternatively, could use in-country reports
            # incountry_reports = content.get("incountry", {}).get("reports", [])
            
            return functional_reports if functional_reports else []
            
        except Exception as e:
            logger.error(f"Error extracting reportees: {str(e)}")
            return []
    
    @staticmethod
    def extract_manager_info(profile_data: Dict) -> Dict:
        """
        Extract manager information from profile
        
        Args:
            profile_data: Full profile response from W3 API
            
        Returns:
            Dict with manager basic info
        """
        try:
            identity_info = profile_data.get("content", {}).get("identity_info", {}).get("content", {})
            
            return {
                "user_id": profile_data.get("userId"),
                "name": identity_info.get("nameDisplay"),
                "email": identity_info.get("preferredIdentity"),
                "is_manager": identity_info.get("employeeType", {}).get("isManager", False),
                "department": identity_info.get("dept", {}).get("code"),
                "organization": identity_info.get("org", {}).get("title"),
            }
        except Exception as e:
            logger.error(f"Error extracting manager info: {str(e)}")
            return {}
