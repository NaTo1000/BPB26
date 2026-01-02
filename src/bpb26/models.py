"""
Core data models for the Pinnacle Building Compliance Platform
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ComplianceStatus(str, Enum):
    """Compliance status enumeration"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    NEEDS_REVIEW = "needs_review"
    PENDING = "pending"
    UNKNOWN = "unknown"


class ViolationSeverity(str, Enum):
    """Severity level of compliance violations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class RegulationType(str, Enum):
    """Types of building regulations"""
    BUILDING_CODE = "building_code"
    FIRE_SAFETY = "fire_safety"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    STRUCTURAL = "structural"
    ACCESSIBILITY = "accessibility"
    ENERGY = "energy"
    ENVIRONMENTAL = "environmental"
    ZONING = "zoning"


class Regulation(BaseModel):
    """Building regulation model"""
    id: str = Field(..., description="Unique regulation identifier")
    code: str = Field(..., description="Regulation code (e.g., IBC 2021)")
    section: str = Field(..., description="Section number")
    title: str = Field(..., description="Regulation title")
    description: str = Field(..., description="Full regulation text")
    regulation_type: RegulationType
    jurisdiction: str = Field(..., description="Geographic jurisdiction")
    effective_date: datetime
    version: str = Field(default="1.0")
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ComplianceViolation(BaseModel):
    """Compliance violation model"""
    id: str = Field(..., description="Unique violation identifier")
    regulation_id: str = Field(..., description="Related regulation ID")
    severity: ViolationSeverity
    description: str = Field(..., description="Violation description")
    location: Optional[str] = Field(None, description="Location in document/plan")
    detected_at: datetime = Field(default_factory=datetime.now)
    recommendations: List[str] = Field(default_factory=list)
    auto_fixable: bool = Field(default=False)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BuildingProject(BaseModel):
    """Building project model"""
    id: str = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Project name")
    address: str = Field(..., description="Project address")
    project_type: str = Field(..., description="Type of building project")
    jurisdiction: str = Field(..., description="Geographic jurisdiction")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    status: ComplianceStatus = Field(default=ComplianceStatus.PENDING)
    violations: List[ComplianceViolation] = Field(default_factory=list)
    compliance_score: float = Field(default=0.0, ge=0.0, le=100.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ComplianceReport(BaseModel):
    """Compliance analysis report"""
    project_id: str
    generated_at: datetime = Field(default_factory=datetime.now)
    overall_status: ComplianceStatus
    compliance_score: float = Field(..., ge=0.0, le=100.0)
    total_violations: int = Field(default=0)
    violations_by_severity: Dict[ViolationSeverity, int] = Field(default_factory=dict)
    violations: List[ComplianceViolation] = Field(default_factory=list)
    applicable_regulations: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    summary: str = Field(default="")


class AIInsight(BaseModel):
    """AI-generated insight model"""
    id: str = Field(..., description="Unique insight identifier")
    project_id: str
    insight_type: str = Field(..., description="Type of insight")
    title: str
    description: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    generated_at: datetime = Field(default_factory=datetime.now)
    recommendations: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
