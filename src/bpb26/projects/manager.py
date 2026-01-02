"""
Project Manager - Building project lifecycle management

This module manages the lifecycle of building projects including:
- Project creation and tracking
- Inspection workflow management
- Permit lifecycle management
- Progress monitoring and reporting
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from ..models import (
    BuildingProject,
    ComplianceStatus,
    ComplianceViolation,
    ViolationSeverity
)


class ProjectManager:
    """
    Manager for building project lifecycle and compliance tracking.
    """

    def __init__(self):
        """Initialize the project manager."""
        self.projects = {}  # In-memory storage (placeholder)

    def create_project(
        self,
        name: str,
        address: str,
        project_type: str,
        jurisdiction: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> BuildingProject:
        """
        Create a new building project.

        Args:
            name: Project name
            address: Project address
            project_type: Type of building project
            jurisdiction: Geographic jurisdiction
            metadata: Optional additional project metadata

        Returns:
            Created BuildingProject
        """
        project_id = str(uuid.uuid4())
        
        project = BuildingProject(
            id=project_id,
            name=name,
            address=address,
            project_type=project_type,
            jurisdiction=jurisdiction,
            metadata=metadata or {}
        )

        self.projects[project_id] = project
        return project

    def get_project(self, project_id: str) -> Optional[BuildingProject]:
        """
        Retrieve a project by ID.

        Args:
            project_id: Unique project identifier

        Returns:
            BuildingProject if found, None otherwise
        """
        return self.projects.get(project_id)

    def update_project(
        self,
        project_id: str,
        updates: Dict[str, Any]
    ) -> Optional[BuildingProject]:
        """
        Update project information.

        Args:
            project_id: Project ID to update
            updates: Dictionary of fields to update

        Returns:
            Updated BuildingProject if found, None otherwise
        """
        project = self.projects.get(project_id)
        if not project:
            return None

        # Update allowed fields
        allowed_fields = ["name", "address", "status", "metadata", "compliance_score"]
        for field, value in updates.items():
            if field in allowed_fields and hasattr(project, field):
                if field == "metadata":
                    # Merge metadata
                    project.metadata.update(value)
                else:
                    setattr(project, field, value)

        project.updated_at = datetime.now()
        return project

    def add_violation(
        self,
        project_id: str,
        violation: ComplianceViolation
    ) -> bool:
        """
        Add a compliance violation to a project.

        Args:
            project_id: Project ID
            violation: ComplianceViolation to add

        Returns:
            True if successful, False if project not found
        """
        project = self.projects.get(project_id)
        if not project:
            return False

        project.violations.append(violation)
        project.updated_at = datetime.now()
        
        # Update project status based on violations
        self._update_project_status(project)
        
        return True

    def remove_violation(
        self,
        project_id: str,
        violation_id: str
    ) -> bool:
        """
        Remove a violation from a project (when resolved).

        Args:
            project_id: Project ID
            violation_id: Violation ID to remove

        Returns:
            True if successful, False if not found
        """
        project = self.projects.get(project_id)
        if not project:
            return False

        # Find and remove violation
        original_count = len(project.violations)
        project.violations = [
            v for v in project.violations if v.id != violation_id
        ]

        if len(project.violations) < original_count:
            project.updated_at = datetime.now()
            self._update_project_status(project)
            return True

        return False

    def _update_project_status(self, project: BuildingProject):
        """
        Update project compliance status based on violations.

        Args:
            project: BuildingProject to update
        """
        if not project.violations:
            project.status = ComplianceStatus.COMPLIANT
            return

        # Check for critical violations
        has_critical = any(
            v.severity == ViolationSeverity.CRITICAL 
            for v in project.violations
        )

        if has_critical:
            project.status = ComplianceStatus.NON_COMPLIANT
        else:
            project.status = ComplianceStatus.NEEDS_REVIEW

    def list_projects(
        self,
        status: Optional[ComplianceStatus] = None,
        jurisdiction: Optional[str] = None
    ) -> List[BuildingProject]:
        """
        List all projects with optional filters.

        Args:
            status: Optional status filter
            jurisdiction: Optional jurisdiction filter

        Returns:
            List of BuildingProjects
        """
        projects = list(self.projects.values())

        if status:
            projects = [p for p in projects if p.status == status]

        if jurisdiction:
            projects = [p for p in projects if p.jurisdiction.lower() == jurisdiction.lower()]

        return projects

    def get_project_summary(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a summary of project status and compliance.

        Args:
            project_id: Project ID

        Returns:
            Dictionary with project summary if found, None otherwise
        """
        project = self.projects.get(project_id)
        if not project:
            return None
        
        # Count violations by severity
        violation_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }

        for violation in project.violations:
            severity_key = violation.severity.value
            violation_counts[severity_key] = violation_counts.get(severity_key, 0) + 1

        summary = {
            "project_id": project.id,
            "name": project.name,
            "address": project.address,
            "status": project.status.value,
            "compliance_score": project.compliance_score,
            "total_violations": len(project.violations),
            "violations_by_severity": violation_counts,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat(),
        }

        return summary

    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project.

        Args:
            project_id: Project ID to delete

        Returns:
            True if successful, False if not found
        """
        if project_id in self.projects:
            del self.projects[project_id]
            return True
        return False

    def search_projects(
        self,
        query: str,
        search_fields: Optional[List[str]] = None
    ) -> List[BuildingProject]:
        """
        Search projects by text query.

        Args:
            query: Search query string
            search_fields: Optional list of fields to search in

        Returns:
            List of matching BuildingProjects
        """
        if not search_fields:
            search_fields = ["name", "address", "project_type"]

        query_lower = query.lower()
        results = []

        for project in self.projects.values():
            for field in search_fields:
                if hasattr(project, field):
                    value = str(getattr(project, field)).lower()
                    if query_lower in value:
                        results.append(project)
                        break

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall project statistics.

        Returns:
            Dictionary with project statistics
        """
        total_projects = len(self.projects)
        
        status_counts = {}
        for project in self.projects.values():
            status = project.status.value
            status_counts[status] = status_counts.get(status, 0) + 1

        total_violations = sum(
            len(p.violations) for p in self.projects.values()
        )

        avg_compliance_score = 0.0
        if total_projects > 0:
            avg_compliance_score = sum(
                p.compliance_score for p in self.projects.values()
            ) / total_projects

        return {
            "total_projects": total_projects,
            "projects_by_status": status_counts,
            "total_violations": total_violations,
            "average_compliance_score": round(avg_compliance_score, 2)
        }
