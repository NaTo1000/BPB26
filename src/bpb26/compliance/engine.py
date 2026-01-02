"""
Compliance Engine - Core compliance checking functionality

This module provides the main compliance checking engine that analyzes
building projects against applicable regulations.
"""
from typing import List, Dict, Optional
from datetime import datetime
import uuid

from ..models import (
    BuildingProject,
    ComplianceReport,
    ComplianceViolation,
    ComplianceStatus,
    ViolationSeverity,
    Regulation
)


class ComplianceEngine:
    """
    Main compliance checking engine that evaluates building projects
    against applicable regulations and standards.
    """

    def __init__(self, regulation_db=None):
        """
        Initialize the compliance engine.

        Args:
            regulation_db: Optional RegulationDatabase instance
        """
        self.regulation_db = regulation_db
        self.violation_rules = self._initialize_violation_rules()

    def _initialize_violation_rules(self) -> Dict:
        """Initialize built-in violation detection rules"""
        return {
            "structural": {
                "min_foundation_depth": 42,  # inches
                "max_wall_height": 120,  # feet
                "min_beam_size": 4,  # inches
            },
            "fire_safety": {
                "max_exit_distance": 200,  # feet
                "min_exit_width": 36,  # inches
                "sprinkler_required": True,
            },
            "accessibility": {
                "min_door_width": 32,  # inches
                "max_ramp_slope": 12,  # ratio (1:12)
                "min_clearance": 60,  # inches
            },
            "energy": {
                "min_insulation_r_value": 13,
                "max_window_u_factor": 0.35,
            }
        }

    def check_compliance(
        self, 
        project: BuildingProject,
        regulations: Optional[List[Regulation]] = None
    ) -> ComplianceReport:
        """
        Check compliance for a building project.

        Args:
            project: BuildingProject to check
            regulations: Optional list of specific regulations to check against

        Returns:
            ComplianceReport with violations and compliance status
        """
        violations = []
        applicable_regulations = []

        # Get applicable regulations from database if available
        if self.regulation_db and not regulations:
            regulations = self.regulation_db.get_applicable_regulations(
                jurisdiction=project.jurisdiction,
                project_type=project.project_type
            )

        if regulations:
            applicable_regulations = [reg.id for reg in regulations]
            # Check each regulation
            for regulation in regulations:
                violation = self._check_regulation(project, regulation)
                if violation:
                    violations.append(violation)

        # Perform automated checks based on built-in rules
        auto_violations = self._perform_automated_checks(project)
        violations.extend(auto_violations)

        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(violations)

        # Determine overall status
        overall_status = self._determine_status(violations, compliance_score)

        # Count violations by severity
        violations_by_severity = {}
        for violation in violations:
            severity = violation.severity
            violations_by_severity[severity] = violations_by_severity.get(severity, 0) + 1

        # Generate recommendations
        recommendations = self._generate_recommendations(violations)

        # Create report
        report = ComplianceReport(
            project_id=project.id,
            overall_status=overall_status,
            compliance_score=compliance_score,
            total_violations=len(violations),
            violations_by_severity=violations_by_severity,
            violations=violations,
            applicable_regulations=applicable_regulations,
            recommendations=recommendations,
            summary=self._generate_summary(violations, compliance_score)
        )

        return report

    def _check_regulation(
        self,
        project: BuildingProject,
        regulation: Regulation
    ) -> Optional[ComplianceViolation]:
        """
        Check a specific regulation against a project.

        Args:
            project: BuildingProject to check
            regulation: Regulation to check against

        Returns:
            ComplianceViolation if non-compliant, None otherwise
        """
        # This is a placeholder for actual regulation checking logic
        # In a real implementation, this would involve sophisticated
        # analysis of project documents and plans
        return None

    def _perform_automated_checks(
        self,
        project: BuildingProject
    ) -> List[ComplianceViolation]:
        """
        Perform automated compliance checks based on built-in rules.

        Args:
            project: BuildingProject to check

        Returns:
            List of detected violations
        """
        violations = []

        # Example automated checks
        # In a real implementation, these would analyze actual project data
        
        # Check for required metadata
        if not project.metadata.get("building_height"):
            violations.append(ComplianceViolation(
                id=str(uuid.uuid4()),
                regulation_id="GENERAL-001",
                severity=ViolationSeverity.MEDIUM,
                description="Building height not specified in project metadata",
                recommendations=[
                    "Specify building height in project metadata",
                    "Ensure height complies with zoning regulations"
                ]
            ))

        # Check for emergency exit information
        if not project.metadata.get("emergency_exits"):
            violations.append(ComplianceViolation(
                id=str(uuid.uuid4()),
                regulation_id="FIRE-001",
                severity=ViolationSeverity.HIGH,
                description="Emergency exit information not provided",
                recommendations=[
                    "Document all emergency exits",
                    "Ensure exits meet minimum width requirements",
                    "Verify exit distances comply with fire safety codes"
                ]
            ))

        return violations

    def _calculate_compliance_score(self, violations: List[ComplianceViolation]) -> float:
        """
        Calculate overall compliance score based on violations.

        Args:
            violations: List of detected violations

        Returns:
            Compliance score (0-100)
        """
        if not violations:
            return 100.0

        # Weight violations by severity
        severity_weights = {
            ViolationSeverity.CRITICAL: 20,
            ViolationSeverity.HIGH: 10,
            ViolationSeverity.MEDIUM: 5,
            ViolationSeverity.LOW: 2,
            ViolationSeverity.INFO: 1,
        }

        total_deduction = sum(
            severity_weights.get(v.severity, 5) for v in violations
        )

        # Calculate score (100 - deductions, minimum 0)
        score = max(0.0, 100.0 - total_deduction)
        return round(score, 2)

    def _determine_status(
        self,
        violations: List[ComplianceViolation],
        score: float
    ) -> ComplianceStatus:
        """
        Determine overall compliance status.

        Args:
            violations: List of violations
            score: Compliance score

        Returns:
            ComplianceStatus
        """
        if not violations:
            return ComplianceStatus.COMPLIANT

        # Check for critical violations
        has_critical = any(
            v.severity == ViolationSeverity.CRITICAL for v in violations
        )
        if has_critical:
            return ComplianceStatus.NON_COMPLIANT

        # Check score thresholds
        if score >= 90:
            return ComplianceStatus.NEEDS_REVIEW
        elif score >= 70:
            return ComplianceStatus.NEEDS_REVIEW
        else:
            return ComplianceStatus.NON_COMPLIANT

    def _generate_recommendations(
        self,
        violations: List[ComplianceViolation]
    ) -> List[str]:
        """
        Generate high-level recommendations based on violations.

        Args:
            violations: List of violations

        Returns:
            List of recommendations
        """
        recommendations = []

        if not violations:
            recommendations.append("Project appears compliant with all checked regulations")
            return recommendations

        # Aggregate recommendations from violations
        for violation in violations:
            recommendations.extend(violation.recommendations)

        # Add general recommendations based on violation patterns
        critical_count = sum(
            1 for v in violations if v.severity == ViolationSeverity.CRITICAL
        )
        if critical_count > 0:
            recommendations.insert(
                0,
                f"Address {critical_count} critical violation(s) immediately before proceeding"
            )

        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)

        return unique_recommendations[:10]  # Limit to top 10

    def _generate_summary(self, violations: List[ComplianceViolation], score: float) -> str:
        """
        Generate a summary of the compliance check.

        Args:
            violations: List of violations
            score: Compliance score

        Returns:
            Summary string
        """
        if not violations:
            return f"Compliance check completed successfully. Score: {score}/100. No violations detected."

        critical_count = sum(1 for v in violations if v.severity == ViolationSeverity.CRITICAL)
        high_count = sum(1 for v in violations if v.severity == ViolationSeverity.HIGH)
        
        summary = f"Compliance check identified {len(violations)} violation(s). Score: {score}/100. "
        
        if critical_count > 0:
            summary += f"{critical_count} critical, "
        if high_count > 0:
            summary += f"{high_count} high priority. "
        
        summary += "Review and address violations before proceeding."
        
        return summary
