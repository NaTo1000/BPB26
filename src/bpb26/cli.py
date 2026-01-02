"""
Command Line Interface for Pinnacle Building Compliance Platform
"""
import argparse
import sys
import json
from typing import Optional

from ..compliance.engine import ComplianceEngine
from ..ai.analyzer import AIAnalyzer
from ..regulations.database import RegulationDatabase
from ..projects.manager import ProjectManager
from ..models import ComplianceStatus


class CLI:
    """Command line interface for BPB26"""

    def __init__(self):
        self.regulation_db = RegulationDatabase()
        self.compliance_engine = ComplianceEngine(regulation_db=self.regulation_db)
        self.ai_analyzer = AIAnalyzer()
        self.project_manager = ProjectManager()

    def create_project(self, args):
        """Create a new project"""
        project = self.project_manager.create_project(
            name=args.name,
            address=args.address,
            project_type=args.type,
            jurisdiction=args.jurisdiction,
            metadata={}
        )
        print(f"✓ Project created successfully!")
        print(f"  ID: {project.id}")
        print(f"  Name: {project.name}")
        print(f"  Address: {project.address}")
        print(f"  Type: {project.project_type}")
        print(f"  Jurisdiction: {project.jurisdiction}")

    def list_projects(self, args):
        """List all projects"""
        projects = self.project_manager.list_projects()
        
        if not projects:
            print("No projects found.")
            return

        print(f"\n{'ID':<38} {'Name':<30} {'Status':<15} {'Score':<8}")
        print("-" * 95)
        for project in projects:
            print(f"{project.id:<38} {project.name:<30} {project.status.value:<15} {project.compliance_score:<8.2f}")
        print(f"\nTotal projects: {len(projects)}")

    def check_compliance(self, args):
        """Check compliance for a project"""
        project = self.project_manager.get_project(args.project_id)
        if not project:
            print(f"Error: Project {args.project_id} not found")
            return

        print(f"\nRunning compliance check for: {project.name}")
        print("-" * 60)

        report = self.compliance_engine.check_compliance(project)

        # Update project
        self.project_manager.update_project(
            project.id,
            {
                "status": report.overall_status,
                "compliance_score": report.compliance_score
            }
        )

        # Display results
        print(f"\n{'Compliance Score:':<25} {report.compliance_score:.2f}/100")
        print(f"{'Overall Status:':<25} {report.overall_status.value}")
        print(f"{'Total Violations:':<25} {report.total_violations}")
        
        if report.violations_by_severity:
            print(f"\n{'Violations by Severity:':}")
            for severity, count in report.violations_by_severity.items():
                print(f"  {severity.value:<15} {count}")

        if report.violations:
            print(f"\n{'Violations:':}")
            for i, violation in enumerate(report.violations, 1):
                print(f"\n  {i}. [{violation.severity.value.upper()}] {violation.description}")
                if violation.recommendations:
                    print(f"     Recommendations:")
                    for rec in violation.recommendations[:3]:
                        print(f"       - {rec}")

        if report.recommendations:
            print(f"\n{'Top Recommendations:':}")
            for i, rec in enumerate(report.recommendations[:5], 1):
                print(f"  {i}. {rec}")

        print(f"\n{report.summary}")

    def search_regulations(self, args):
        """Search regulations"""
        regulations = self.regulation_db.search_regulations(
            query=args.query,
            jurisdiction=args.jurisdiction
        )

        if not regulations:
            print(f"No regulations found for query: {args.query}")
            return

        print(f"\nFound {len(regulations)} regulation(s):\n")
        for reg in regulations:
            print(f"ID: {reg.id}")
            print(f"Code: {reg.code} - Section {reg.section}")
            print(f"Title: {reg.title}")
            print(f"Type: {reg.regulation_type.value}")
            print(f"Jurisdiction: {reg.jurisdiction}")
            print(f"Description: {reg.description[:150]}...")
            print("-" * 60)

    def analyze_project(self, args):
        """Generate AI insights for a project"""
        project = self.project_manager.get_project(args.project_id)
        if not project:
            print(f"Error: Project {args.project_id} not found")
            return

        print(f"\nGenerating AI insights for: {project.name}")
        print("-" * 60)

        insights = self.ai_analyzer.predict_compliance_issues(project)

        if not insights:
            print("No insights generated.")
            return

        for i, insight in enumerate(insights, 1):
            print(f"\n{i}. {insight.title}")
            print(f"   Type: {insight.insight_type}")
            print(f"   Confidence: {insight.confidence:.2%}")
            print(f"   {insight.description}")
            if insight.recommendations:
                print(f"   Recommendations:")
                for rec in insight.recommendations:
                    print(f"     - {rec}")

    def show_statistics(self, args):
        """Show platform statistics"""
        stats = self.project_manager.get_statistics()
        
        print("\n=== Platform Statistics ===\n")
        print(f"Total Projects: {stats['total_projects']}")
        print(f"Average Compliance Score: {stats['average_compliance_score']:.2f}")
        print(f"Total Violations: {stats['total_violations']}")
        
        if stats['projects_by_status']:
            print("\nProjects by Status:")
            for status, count in stats['projects_by_status'].items():
                print(f"  {status:<20} {count}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Pinnacle Building Compliance Platform CLI",
        prog="bpb26"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create project command
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument("--name", required=True, help="Project name")
    create_parser.add_argument("--address", required=True, help="Project address")
    create_parser.add_argument("--type", required=True, help="Project type")
    create_parser.add_argument("--jurisdiction", required=True, help="Jurisdiction")

    # List projects command
    list_parser = subparsers.add_parser("list", help="List all projects")

    # Check compliance command
    check_parser = subparsers.add_parser("check", help="Check project compliance")
    check_parser.add_argument("project_id", help="Project ID to check")

    # Search regulations command
    search_parser = subparsers.add_parser("search", help="Search regulations")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--jurisdiction", help="Filter by jurisdiction")

    # Analyze project command
    analyze_parser = subparsers.add_parser("analyze", help="Generate AI insights")
    analyze_parser.add_argument("project_id", help="Project ID to analyze")

    # Statistics command
    stats_parser = subparsers.add_parser("stats", help="Show platform statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = CLI()

    # Execute command
    if args.command == "create":
        cli.create_project(args)
    elif args.command == "list":
        cli.list_projects(args)
    elif args.command == "check":
        cli.check_compliance(args)
    elif args.command == "search":
        cli.search_regulations(args)
    elif args.command == "analyze":
        cli.analyze_project(args)
    elif args.command == "stats":
        cli.show_statistics(args)


if __name__ == "__main__":
    main()
