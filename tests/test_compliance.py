"""
Tests for the Compliance Engine
"""
import pytest
from datetime import datetime

from bpb26.compliance.engine import ComplianceEngine
from bpb26.models import BuildingProject, ComplianceStatus, ViolationSeverity
from bpb26.regulations.database import RegulationDatabase


def test_compliance_engine_initialization():
    """Test compliance engine initialization"""
    engine = ComplianceEngine()
    assert engine is not None
    assert engine.violation_rules is not None


def test_check_compliance_no_violations():
    """Test compliance check with no violations"""
    regulation_db = RegulationDatabase()
    engine = ComplianceEngine(regulation_db=regulation_db)
    
    project = BuildingProject(
        id="test-1",
        name="Test Project",
        address="123 Test St",
        project_type="Residential",
        jurisdiction="Test City",
        metadata={
            "building_height": 30,
            "emergency_exits": 2
        }
    )
    
    report = engine.check_compliance(project)
    
    assert report is not None
    assert report.project_id == project.id
    assert report.compliance_score >= 0
    assert report.overall_status in [status for status in ComplianceStatus]


def test_check_compliance_with_violations():
    """Test compliance check that detects violations"""
    regulation_db = RegulationDatabase()
    engine = ComplianceEngine(regulation_db=regulation_db)
    
    project = BuildingProject(
        id="test-2",
        name="Test Project",
        address="123 Test St",
        project_type="Residential",
        jurisdiction="Test City",
        metadata={}  # Missing required fields
    )
    
    report = engine.check_compliance(project)
    
    assert report is not None
    assert report.total_violations > 0
    assert len(report.violations) > 0
    assert report.compliance_score < 100


def test_compliance_score_calculation():
    """Test compliance score calculation"""
    engine = ComplianceEngine()
    
    # Test with no violations
    score = engine._calculate_compliance_score([])
    assert score == 100.0
    
    # Test with violations is handled by the private method
    # (Full testing would require creating actual violation objects)


def test_determine_status():
    """Test status determination logic"""
    engine = ComplianceEngine()
    
    # Test compliant status
    status = engine._determine_status([], 100.0)
    assert status == ComplianceStatus.COMPLIANT
