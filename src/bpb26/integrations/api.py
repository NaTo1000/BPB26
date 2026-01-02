"""
FastAPI Application - RESTful API for Pinnacle Building Compliance Platform

This module provides REST API endpoints for all platform functionality.
"""
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..models import (
    BuildingProject,
    ComplianceReport,
    Regulation,
    ComplianceStatus,
    RegulationType,
    AIInsight
)
from ..compliance.engine import ComplianceEngine
from ..ai.analyzer import AIAnalyzer
from ..regulations.database import RegulationDatabase
from ..projects.manager import ProjectManager


# Request/Response Models
class ProjectCreateRequest(BaseModel):
    """Request model for creating a project"""
    name: str
    address: str
    project_type: str
    jurisdiction: str
    metadata: dict = {}


class ComplianceCheckRequest(BaseModel):
    """Request model for compliance check"""
    project_id: str
    regulation_ids: Optional[List[str]] = None


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="Pinnacle Building Compliance Platform API",
        description="AI-powered building compliance and regulation management",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize components
    regulation_db = RegulationDatabase()
    compliance_engine = ComplianceEngine(regulation_db=regulation_db)
    ai_analyzer = AIAnalyzer()
    project_manager = ProjectManager()

    # Store in app state
    app.state.regulation_db = regulation_db
    app.state.compliance_engine = compliance_engine
    app.state.ai_analyzer = ai_analyzer
    app.state.project_manager = project_manager

    # Routes
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "name": "Pinnacle Building Compliance Platform",
            "version": "1.0.0",
            "status": "operational",
            "message": "AI-powered building compliance and regulation management"
        }

    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy"}

    # Project endpoints
    @app.post("/api/projects", response_model=BuildingProject)
    async def create_project(request: ProjectCreateRequest):
        """Create a new building project"""
        project = project_manager.create_project(
            name=request.name,
            address=request.address,
            project_type=request.project_type,
            jurisdiction=request.jurisdiction,
            metadata=request.metadata
        )
        return project

    @app.get("/api/projects/{project_id}", response_model=BuildingProject)
    async def get_project(project_id: str):
        """Get project by ID"""
        project = project_manager.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    @app.get("/api/projects", response_model=List[BuildingProject])
    async def list_projects(
        status: Optional[ComplianceStatus] = Query(None),
        jurisdiction: Optional[str] = Query(None)
    ):
        """List all projects with optional filters"""
        projects = project_manager.list_projects(
            status=status,
            jurisdiction=jurisdiction
        )
        return projects

    @app.get("/api/projects/{project_id}/summary")
    async def get_project_summary(project_id: str):
        """Get project summary"""
        summary = project_manager.get_project_summary(project_id)
        if not summary:
            raise HTTPException(status_code=404, detail="Project not found")
        return summary

    @app.delete("/api/projects/{project_id}")
    async def delete_project(project_id: str):
        """Delete a project"""
        success = project_manager.delete_project(project_id)
        if not success:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"status": "deleted", "project_id": project_id}

    # Compliance endpoints
    @app.post("/api/compliance/check", response_model=ComplianceReport)
    async def check_compliance(request: ComplianceCheckRequest):
        """Check project compliance"""
        project = project_manager.get_project(request.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Get specific regulations if requested
        regulations = None
        if request.regulation_ids:
            regulations = [
                regulation_db.get_regulation(reg_id)
                for reg_id in request.regulation_ids
            ]
            regulations = [r for r in regulations if r is not None]

        # Run compliance check
        report = compliance_engine.check_compliance(project, regulations)
        
        # Update project with results
        project_manager.update_project(
            project.id,
            {
                "status": report.overall_status,
                "compliance_score": report.compliance_score
            }
        )

        return report

    # Regulation endpoints
    @app.get("/api/regulations/{regulation_id}", response_model=Regulation)
    async def get_regulation(regulation_id: str):
        """Get regulation by ID"""
        regulation = regulation_db.get_regulation(regulation_id)
        if not regulation:
            raise HTTPException(status_code=404, detail="Regulation not found")
        return regulation

    @app.get("/api/regulations", response_model=List[Regulation])
    async def search_regulations(
        query: Optional[str] = Query(None),
        jurisdiction: Optional[str] = Query(None),
        code: Optional[str] = Query(None),
        regulation_type: Optional[RegulationType] = Query(None)
    ):
        """Search regulations"""
        if query:
            regulations = regulation_db.search_regulations(
                query=query,
                jurisdiction=jurisdiction,
                code=code
            )
        elif regulation_type:
            regulations = regulation_db.get_regulations_by_type(
                regulation_type=regulation_type,
                jurisdiction=jurisdiction
            )
        else:
            # Return all regulations for jurisdiction
            regulations = regulation_db.get_applicable_regulations(
                jurisdiction=jurisdiction or "International"
            )
        return regulations

    @app.get("/api/regulations/codes")
    async def list_codes():
        """List all available building codes"""
        codes = regulation_db.get_all_codes()
        return {"codes": codes}

    @app.get("/api/regulations/jurisdictions")
    async def list_jurisdictions():
        """List all available jurisdictions"""
        jurisdictions = regulation_db.get_all_jurisdictions()
        return {"jurisdictions": jurisdictions}

    # AI endpoints
    @app.post("/api/ai/analyze", response_model=List[AIInsight])
    async def analyze_project(project_id: str):
        """Generate AI insights for a project"""
        project = project_manager.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        insights = ai_analyzer.predict_compliance_issues(project)
        return insights

    @app.post("/api/ai/recommendations")
    async def get_recommendations(project_id: str):
        """Get AI-generated recommendations"""
        project = project_manager.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        recommendations = ai_analyzer.generate_recommendations(
            project=project,
            violations=project.violations
        )
        return {"project_id": project_id, "recommendations": recommendations}

    # Statistics endpoint
    @app.get("/api/statistics")
    async def get_statistics():
        """Get platform statistics"""
        stats = project_manager.get_statistics()
        return stats

    return app


# Create app instance
app = create_app()
