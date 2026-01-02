"""
Pinnacle Building Compliance Platform (BPB26)

A comprehensive AI-powered solution for building industry compliance and regulation management.
"""

__version__ = "1.0.0"
__author__ = "BPB26 Team"

from .compliance.engine import ComplianceEngine
from .ai.analyzer import AIAnalyzer
from .regulations.database import RegulationDatabase
from .projects.manager import ProjectManager

__all__ = [
    "ComplianceEngine",
    "AIAnalyzer",
    "RegulationDatabase",
    "ProjectManager",
]
