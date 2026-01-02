"""
Tests for the Project Manager
"""
import pytest

from bpb26.projects.manager import ProjectManager
from bpb26.models import ComplianceStatus


def test_project_manager_initialization():
    """Test project manager initialization"""
    manager = ProjectManager()
    assert manager is not None
    assert manager.projects == {}


def test_create_project():
    """Test project creation"""
    manager = ProjectManager()
    
    project = manager.create_project(
        name="Test Project",
        address="123 Test St",
        project_type="Residential",
        jurisdiction="Test City"
    )
    
    assert project is not None
    assert project.id is not None
    assert project.name == "Test Project"
    assert project.address == "123 Test St"
    assert project.status == ComplianceStatus.PENDING


def test_get_project():
    """Test retrieving a project"""
    manager = ProjectManager()
    
    project = manager.create_project(
        name="Test Project",
        address="123 Test St",
        project_type="Residential",
        jurisdiction="Test City"
    )
    
    retrieved = manager.get_project(project.id)
    assert retrieved is not None
    assert retrieved.id == project.id


def test_list_projects():
    """Test listing projects"""
    manager = ProjectManager()
    
    # Create multiple projects
    project1 = manager.create_project(
        name="Project 1",
        address="123 Test St",
        project_type="Residential",
        jurisdiction="Test City"
    )
    
    project2 = manager.create_project(
        name="Project 2",
        address="456 Test Ave",
        project_type="Commercial",
        jurisdiction="Test City"
    )
    
    projects = manager.list_projects()
    assert len(projects) == 2


def test_get_statistics():
    """Test getting platform statistics"""
    manager = ProjectManager()
    
    # Create a project
    manager.create_project(
        name="Test Project",
        address="123 Test St",
        project_type="Residential",
        jurisdiction="Test City"
    )
    
    stats = manager.get_statistics()
    assert stats["total_projects"] == 1
    assert "average_compliance_score" in stats
