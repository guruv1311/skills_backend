from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from app.core.database import get_db
from app.models.users import User
from app.models.professional_eminence import ProfessionalEminence
from app.models.user_skills import UserSkill
from app.models.projects import Project
from app.models.assets import Asset
from app.models.user_cert import UserCert
from app.auth.dependencies import get_current_user
from app.services.w3_profile_service import W3ProfileService
import logging
from sqlalchemy import func


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/manager/{manager_id}/reportees")
async def get_manager_reportees(
    manager_id: str,
    include_skills: bool = Query(True, description="Include skills data"),
    include_projects: bool = Query(True, description="Include projects data"),
    include_assets: bool = Query(True, description="Include assets data"),
    include_certifications: bool = Query(True, description="Include certifications data"),
    include_eminence: bool = Query(False, description="Include professional eminence data"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get manager's reportees with their complete information
    
    Workflow:
    1. Fetch manager profile from IBM W3 API
    2. Extract reportee user IDs
    3. Get reportee details from local database
    4. Include assets, skills, projects, certifications as requested
    
    Args:
        manager_id: Manager's user ID
        include_skills: Include skills data
        include_projects: Include project data
        include_assets: Include assets data (default: True)
        include_certifications: Include certification data
        include_eminence: Include professional eminence data (default: False)
    
    Returns:
        Manager info and list of reportees with their complete data
    """
    try:
        # Step 1: Fetch manager profile from W3 API
        logger.info(f"Fetching W3 profile for manager: {manager_id}")
        profile_data = await W3ProfileService.get_user_profile(manager_id)
        
        if not profile_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Manager profile not found in W3 API for user ID: {manager_id}"
            )
        
        # Step 2: Extract manager info
        manager_info = W3ProfileService.extract_manager_info(profile_data)
        
        # Verify user is a manager
        if not manager_info.get("is_manager"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {manager_id} is not a manager"
            )
        
        # Step 3: Extract reportee user IDs
        reportee_ids = W3ProfileService.extract_reportees(profile_data)
        
        if not reportee_ids:
            return {
                "manager": manager_info,
                "reportee_count": 0,
                "reportees": []
            }
        
        logger.info(f"Found {len(reportee_ids)} reportees for manager {manager_id}")
        
        # Step 4: Fetch reportee data from database
        reportees_data = []
        
        for reportee_id in reportee_ids:
            try:
                # Get user from database
                user = db.query(User).filter(User.user_id == reportee_id).first()
                
                if not user:
                    # User not in database yet
                    logger.warning(f"Reportee {reportee_id} not found in database")
                    reportees_data.append({
                        "user_id": reportee_id,
                        "in_database": False,
                        "message": "User not yet registered in system"
                    })
                    continue
                
                # Build reportee data
                reportee_data = {
                    "user_id": user.user_id,
                    "name": user.name,
                    "email": user.email,
                    "user_type": user.user_type,
                    "in_database": True
                }
                
                # Include assets (default)
                if include_assets:
                    assets = db.query(Asset).filter(
                        Asset.user_id == reportee_id
                    ).all()
                    
                    reportee_data["assets"] = [
                        {
                            "id": a.id,
                            "asset_name": a.asset_name,
                            "asset_desc": a.asset_desc,
                            "used_in_project": a.used_in_project,
                            "ai_adoption": a.ai_adoption,
                            "your_contribution": a.your_contribution,
                            "status": a.status,
                            "url": a.url
                        }
                        for a in assets
                    ]
                    reportee_data["assets_count"] = len(assets)
                
                # Include skills
                if include_skills:
                    skills = db.query(UserSkill).filter(
                        UserSkill.user_id == reportee_id
                    ).all()
                    
                    reportee_data["skills"] = [
                        {
                            "id": s.id,
                            "platform": s.platform,
                            "segment": s.segment,
                            "proficiency_level": s.proficiency_level,
                            "skill_type": s.skill_type,
                            "yoe": s.yoe,
                            "status": s.status
                        }
                        for s in skills
                    ]
                    reportee_data["skills_count"] = len(skills)
                
                # Include projects
                if include_projects:
                    projects = db.query(Project).filter(
                        Project.user_id == reportee_id
                    ).all()
                    
                    reportee_data["projects"] = [
                        {
                            "id": p.id,
                            "project_name": p.project_name,
                            "client_name": p.client_name,
                            "your_role": p.your_role,
                            "tech_used": p.tech_used,
                            "is_foak": p.is_foak,
                            "status": p.status,
                            "asset_used": p.asset_used,
                            "asset_name": p.asset_name
                        }
                        for p in projects
                    ]
                    reportee_data["projects_count"] = len(projects)
                
                # Include certifications
                if include_certifications:
                    certs = db.query(UserCert).filter(
                        UserCert.user_id == reportee_id
                    ).all()
                    
                    reportee_data["certifications"] = [
                        {
                            "id": c.id,
                            "cert_name": c.cert_name,
                            "cert_type": c.cert_type,
                            "cert_cat": c.cert_cat,
                            "issue_date": c.issue_date.isoformat() if c.issue_date else None,
                            "status": c.status
                        }
                        for c in certs
                    ]
                    reportee_data["certifications_count"] = len(certs)
                
                # Include professional eminence (optional)
                if include_eminence:
                    eminences = db.query(ProfessionalEminence).filter(
                        ProfessionalEminence.user_id == reportee_id,
                    ).all()
                    
                    reportee_data["professional_eminence"] = [
                        {
                            "id": e.id,
                            "employee_id": e.user_id,
                            "manager_id": e.manager_id,
                            "url": e.url,
                            "eminence_type": e.eminence_type,
                            "description": e.description,
                            "scope": e.scope
                        }
                        for e in eminences
                    ]
                    reportee_data["eminence_count"] = len(eminences)
                reportees_data.append(reportee_data)
                
            except Exception as e:
                logger.error(f"Error processing reportee {reportee_id}: {str(e)}")
                reportees_data.append({
                    "user_id": reportee_id,
                    "error": str(e),
                    "in_database": False
                })
        
        # Step 5: Return complete response
        return {
            "manager": manager_info,
            "reportee_count": len(reportee_ids),
            "reportees_in_database": len([r for r in reportees_data if r.get("in_database")]),
            "reportees": reportees_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_manager_reportees: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch reportees data"
        )


@router.get("/manager/{manager_id}/reportees/summary")
async def get_reportees_summary(
    manager_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get summary statistics for manager's reportees
    
    Returns:
        Summary of reportees' assets, skills, projects, certifications
    """
    try:
        # Fetch manager profile
        profile_data = await W3ProfileService.get_user_profile(manager_id)
        
        if not profile_data:
            raise HTTPException(status_code=404, detail="Manager not found")
        
        manager_info = W3ProfileService.extract_manager_info(profile_data)
        reportee_ids = W3ProfileService.extract_reportees(profile_data)
        
        if not reportee_ids:
            return {
                "manager": manager_info,
                "summary": {
                    "total_reportees": 0,
                    "reportees_in_system": 0,
                    "total_assets": 0,
                    "total_skills": 0,
                    "total_projects": 0,
                    "total_certifications": 0,
                    "total_eminence_records": 0
                }
            }
        
        # Count reportees in database
        reportees_in_db = db.query(User).filter(User.user_id.in_(reportee_ids)).count()
        
        # Count assets
        total_assets = db.query(Asset).filter(
            Asset.user_id.in_(reportee_ids)
        ).count()
        
        # Count skills
        total_skills = db.query(UserSkill).filter(
            UserSkill.user_id.in_(reportee_ids)
        ).count()
        
        # Count projects
        total_projects = db.query(Project).filter(
            Project.user_id.in_(reportee_ids)
        ).count()
        
        # Count certifications
        total_certs = db.query(UserCert).filter(
            UserCert.user_id.in_(reportee_ids)
        ).count()
        
        # Count eminence records
        total_eminence = db.query(ProfessionalEminence).filter(
            ProfessionalEminence.user_id.in_(reportee_ids)
        ).count()
        
        return {
            "manager": manager_info,
            "summary": {
                "total_reportees": len(reportee_ids),
                "reportees_in_system": reportees_in_db,
                "total_assets": total_assets,
                "total_skills": total_skills,
                "total_projects": total_projects,
                "total_certifications": total_certs,
                "total_eminence_records": total_eminence,
                "reportee_ids": reportee_ids
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_reportees_summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch summary")


@router.get("/manager/{manager_id}/certifications-summary")
async def get_reportees_certifications_summary(
    manager_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get certification counts for manager's reportees
    
    Returns:
        - Total certifications across all reportees
        - Certification count per reportee
        - Breakdown by certification type/category
    """
    try:
        # Fetch manager profile from W3 API
        logger.info(f"Fetching W3 profile for manager: {manager_id}")
        profile_data = await W3ProfileService.get_user_profile(manager_id)
        
        if not profile_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Manager profile not found in W3 API for user ID: {manager_id}"
            )
        
        # Extract manager info and reportees
        manager_info = W3ProfileService.extract_manager_info(profile_data)
        reportee_ids = W3ProfileService.extract_reportees(profile_data)
        
        if not reportee_ids:
            return {
                "manager": manager_info,
                "total_certifications": 0,
                "reportee_count": 0,
                "certifications_by_reportee": [],
                "certifications_by_type": [],
                "certifications_by_category": []
            }
        
        # Get total certification count across all reportees
        total_certs = db.query(func.count(UserCert.id)).filter(
            UserCert.user_id.in_(reportee_ids)
        ).scalar()
        
        # Get certification count per reportee
        certs_by_reportee = db.query(
            UserCert.user_id,
            User.name,
            User.email,
            func.count(UserCert.id).label('cert_count')
        ).join(
            User, User.user_id == UserCert.user_id
        ).filter(
            UserCert.user_id.in_(reportee_ids)
        ).group_by(
            UserCert.user_id, User.name, User.email
        ).all()
        
        # Get certification breakdown by type
        certs_by_type = db.query(
            UserCert.cert_type,
            func.count(UserCert.id).label('count')
        ).filter(
            UserCert.user_id.in_(reportee_ids),
            UserCert.cert_type.isnot(None)
        ).group_by(
            UserCert.cert_type
        ).all()
        
        # Get certification breakdown by category
        certs_by_category = db.query(
            UserCert.cert_cat,
            func.count(UserCert.id).label('count')
        ).filter(
            UserCert.user_id.in_(reportee_ids),
            UserCert.cert_cat.isnot(None)
        ).group_by(
            UserCert.cert_cat
        ).all()
        
        # Format response
        return {
            "manager": manager_info,
            "reportee_count": len(reportee_ids),
            "total_certifications": total_certs or 0,
            "certifications_by_reportee": [
                {
                    "user_id": r.user_id,
                    "name": r.name,
                    "email": r.email,
                    "certification_count": r.cert_count
                }
                for r in certs_by_reportee
            ],
            "certifications_by_type": [
                {
                    "cert_type": t.cert_type,
                    "count": t.count
                }
                for t in certs_by_type
            ],
            "certifications_by_category": [
                {
                    "cert_category": c.cert_cat,
                    "count": c.count
                }
                for c in certs_by_category
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_reportees_certifications_summary: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch certification summary"
        )


@router.get("/manager/{manager_id}/reportees/{reportee_id}/certifications")
async def get_reportee_certifications_detail(
    manager_id: str,
    reportee_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed certifications for a specific reportee
    
    Args:
        manager_id: Manager's user ID
        reportee_id: Reportee's user ID
    
    Returns:
        List of all certifications for the reportee
    """
    try:
        # Verify manager-reportee relationship
        profile_data = await W3ProfileService.get_user_profile(manager_id)
        if not profile_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Manager not found"
            )
        
        reportee_ids = W3ProfileService.extract_reportees(profile_data)
        
        if reportee_id not in reportee_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User {reportee_id} is not a reportee of manager {manager_id}"
            )
        
        # Get reportee's certifications
        certifications = db.query(UserCert).filter(
            UserCert.user_id == reportee_id
        ).all()
        
        # Get user info
        user = db.query(User).filter(User.user_id == reportee_id).first()
        
        return {
            "reportee": {
                "user_id": reportee_id,
                "name": user.name if user else "Unknown",
                "email": user.email if user else "Unknown"
            },
            "certification_count": len(certifications),
            "certifications": [
                {
                    "id": c.id,
                    "cert_name": c.cert_name,
                    "cert_type": c.cert_type,
                    "cert_cat": c.cert_cat,
                    "issue_date": c.issue_date.isoformat() if c.issue_date else None,
                    "status": c.status
                }
                for c in certifications
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_reportee_certifications_detail: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch reportee certifications"
        )
