"""
Example usage of the Pinnacle Building Compliance Platform

This script demonstrates how to use the platform to create projects,
check compliance, and generate insights.
"""

from bpb26.compliance.engine import ComplianceEngine
from bpb26.ai.analyzer import AIAnalyzer
from bpb26.regulations.database import RegulationDatabase
from bpb26.projects.manager import ProjectManager


def main():
    """Demonstrate platform usage"""
    print("=" * 70)
    print("Pinnacle Building Compliance Platform - Example Usage")
    print("=" * 70)

    # Initialize components
    print("\n1. Initializing platform components...")
    regulation_db = RegulationDatabase()
    compliance_engine = ComplianceEngine(regulation_db=regulation_db)
    ai_analyzer = AIAnalyzer()
    project_manager = ProjectManager()
    print("   ✓ Components initialized")

    # Create a sample project
    print("\n2. Creating a sample building project...")
    project = project_manager.create_project(
        name="Downtown Office Tower",
        address="123 Main Street, Seattle, WA 98101",
        project_type="Commercial High-Rise",
        jurisdiction="Seattle, Washington",
        metadata={
            "building_height": 250,
            "floors": 20,
            "square_footage": 150000,
            "occupancy_type": "B - Business",
            "construction_type": "Type I-A"
        }
    )
    print(f"   ✓ Project created: {project.name}")
    print(f"     ID: {project.id}")

    # Search regulations
    print("\n3. Searching applicable regulations...")
    regulations = regulation_db.get_applicable_regulations(
        jurisdiction=project.jurisdiction,
        project_type=project.project_type
    )
    print(f"   ✓ Found {len(regulations)} applicable regulations")
    for reg in regulations[:3]:
        print(f"     - {reg.code} {reg.section}: {reg.title}")

    # Run compliance check
    print("\n4. Running compliance analysis...")
    report = compliance_engine.check_compliance(project, regulations)
    print(f"   ✓ Compliance check completed")
    print(f"     Overall Status: {report.overall_status.value}")
    print(f"     Compliance Score: {report.compliance_score}/100")
    print(f"     Total Violations: {report.total_violations}")

    # Update project with results
    project_manager.update_project(
        project.id,
        {
            "status": report.overall_status,
            "compliance_score": report.compliance_score
        }
    )

    # Display violations if any
    if report.violations:
        print("\n5. Detected Violations:")
        for i, violation in enumerate(report.violations, 1):
            print(f"   {i}. [{violation.severity.value.upper()}] {violation.description}")

    # Display recommendations
    if report.recommendations:
        print("\n6. Recommendations:")
        for i, rec in enumerate(report.recommendations[:5], 1):
            print(f"   {i}. {rec}")

    # Generate AI insights
    print("\n7. Generating AI insights...")
    insights = ai_analyzer.predict_compliance_issues(project)
    print(f"   ✓ Generated {len(insights)} insight(s)")
    for insight in insights:
        print(f"     - {insight.title} (Confidence: {insight.confidence:.0%})")
        print(f"       {insight.description}")

    # Get AI recommendations
    ai_recommendations = ai_analyzer.generate_recommendations(
        project=project,
        violations=report.violations
    )
    print("\n8. AI-Generated Recommendations:")
    for i, rec in enumerate(ai_recommendations[:3], 1):
        print(f"   {i}. {rec}")

    # Show project summary
    print("\n9. Project Summary:")
    summary = project_manager.get_project_summary(project.id)
    print(f"   Name: {summary['name']}")
    print(f"   Status: {summary['status']}")
    print(f"   Compliance Score: {summary['compliance_score']}/100")
    print(f"   Total Violations: {summary['total_violations']}")

    # Platform statistics
    print("\n10. Platform Statistics:")
    stats = project_manager.get_statistics()
    print(f"   Total Projects: {stats['total_projects']}")
    print(f"   Average Compliance Score: {stats['average_compliance_score']}")

    print("\n" + "=" * 70)
    print("Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
