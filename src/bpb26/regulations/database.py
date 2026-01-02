"""
Regulation Database - Centralized storage and retrieval of building regulations

This module manages the storage, versioning, and retrieval of building codes
and regulations from multiple jurisdictions.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from ..models import Regulation, RegulationType


class RegulationDatabase:
    """
    Database for storing and managing building regulations and codes.
    
    Supports multiple jurisdictions, code versions, and regulation types.
    """

    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize the regulation database.

        Args:
            connection_string: Optional database connection string
        """
        self.connection_string = connection_string
        self.regulations = {}  # In-memory storage (placeholder)
        self._initialize_sample_regulations()

    def _initialize_sample_regulations(self):
        """Initialize sample regulations for demonstration"""
        sample_regulations = [
            Regulation(
                id="IBC-2021-1003.2",
                code="IBC 2021",
                section="1003.2",
                title="Ceiling Height",
                description="The minimum ceiling height shall be 7 feet 6 inches (2286 mm). "
                           "Exceptions: Specific areas may have reduced ceiling heights as specified in other sections.",
                regulation_type=RegulationType.BUILDING_CODE,
                jurisdiction="International",
                effective_date=datetime(2021, 1, 1),
                version="2021",
                tags=["ceiling", "height", "interior", "dimensions"]
            ),
            Regulation(
                id="IBC-2021-1009.1",
                code="IBC 2021",
                section="1009.1",
                title="Exit Access Requirements",
                description="Exits shall be continuous from the point of entry to the exit discharge. "
                           "Exit access shall not pass through more than one adjacent space.",
                regulation_type=RegulationType.FIRE_SAFETY,
                jurisdiction="International",
                effective_date=datetime(2021, 1, 1),
                version="2021",
                tags=["exits", "fire safety", "access", "egress"]
            ),
            Regulation(
                id="ADA-2010-404.2.3",
                code="ADA 2010",
                section="404.2.3",
                title="Clear Width of Doorways",
                description="Door openings shall provide a clear width of 32 inches (815 mm) minimum. "
                           "Clear openings of doorways with swinging doors shall be measured between the face "
                           "of the door and the stop, with the door open 90 degrees.",
                regulation_type=RegulationType.ACCESSIBILITY,
                jurisdiction="United States",
                effective_date=datetime(2010, 3, 15),
                version="2010",
                tags=["accessibility", "doors", "clearance", "ADA"]
            ),
            Regulation(
                id="NEC-2020-210.8",
                code="NEC 2020",
                section="210.8",
                title="Ground-Fault Circuit-Interrupter Protection for Personnel",
                description="All 125-volt, single-phase, 15- and 20-ampere receptacles installed in "
                           "bathrooms, garages, outdoors, crawl spaces, and unfinished basements shall have "
                           "ground-fault circuit-interrupter protection for personnel.",
                regulation_type=RegulationType.ELECTRICAL,
                jurisdiction="United States",
                effective_date=datetime(2020, 1, 1),
                version="2020",
                tags=["electrical", "GFCI", "safety", "receptacles"]
            ),
            Regulation(
                id="IPC-2021-305.4",
                code="IPC 2021",
                section="305.4",
                title="Plumbing in Shaft Enclosures",
                description="Plumbing systems shall not be located in an elevator shaft. "
                           "Water, soil and waste piping shall be permitted in plumbing shafts.",
                regulation_type=RegulationType.PLUMBING,
                jurisdiction="International",
                effective_date=datetime(2021, 1, 1),
                version="2021",
                tags=["plumbing", "shafts", "elevators", "piping"]
            ),
            Regulation(
                id="IECC-2021-R402.1.2",
                code="IECC 2021",
                section="R402.1.2",
                title="Insulation Requirements",
                description="The building thermal envelope shall meet the requirements of Table R402.1.2 "
                           "based on climate zone. Insulation R-values shall be certified.",
                regulation_type=RegulationType.ENERGY,
                jurisdiction="International",
                effective_date=datetime(2021, 1, 1),
                version="2021",
                tags=["energy", "insulation", "thermal", "efficiency"]
            ),
        ]

        # Store regulations in memory
        for reg in sample_regulations:
            self.regulations[reg.id] = reg

    def add_regulation(self, regulation: Regulation) -> bool:
        """
        Add a new regulation to the database.

        Args:
            regulation: Regulation to add

        Returns:
            True if successful, False otherwise
        """
        if regulation.id in self.regulations:
            return False
        
        self.regulations[regulation.id] = regulation
        return True

    def get_regulation(self, regulation_id: str) -> Optional[Regulation]:
        """
        Retrieve a specific regulation by ID.

        Args:
            regulation_id: Unique regulation identifier

        Returns:
            Regulation if found, None otherwise
        """
        return self.regulations.get(regulation_id)

    def get_applicable_regulations(
        self,
        jurisdiction: str,
        project_type: Optional[str] = None,
        regulation_types: Optional[List[RegulationType]] = None
    ) -> List[Regulation]:
        """
        Get regulations applicable to a specific jurisdiction and project.

        Args:
            jurisdiction: Geographic jurisdiction
            project_type: Optional project type filter
            regulation_types: Optional list of regulation types to include

        Returns:
            List of applicable regulations
        """
        applicable = []

        for regulation in self.regulations.values():
            # Check jurisdiction match (include "International" as applicable to all)
            if regulation.jurisdiction.lower() != "international" and \
               regulation.jurisdiction.lower() not in jurisdiction.lower():
                continue

            # Check regulation type filter
            if regulation_types and regulation.regulation_type not in regulation_types:
                continue

            applicable.append(regulation)

        return applicable

    def search_regulations(
        self,
        query: str,
        jurisdiction: Optional[str] = None,
        code: Optional[str] = None
    ) -> List[Regulation]:
        """
        Search regulations by text query.

        Args:
            query: Search query string
            jurisdiction: Optional jurisdiction filter
            code: Optional code filter (e.g., "IBC 2021")

        Returns:
            List of matching regulations
        """
        results = []
        query_lower = query.lower()

        for regulation in self.regulations.values():
            # Apply filters
            if jurisdiction and regulation.jurisdiction.lower() != jurisdiction.lower():
                continue
            if code and regulation.code.lower() != code.lower():
                continue

            # Search in title, description, and tags
            if (query_lower in regulation.title.lower() or
                query_lower in regulation.description.lower() or
                any(query_lower in tag.lower() for tag in regulation.tags)):
                results.append(regulation)

        return results

    def get_regulations_by_type(
        self,
        regulation_type: RegulationType,
        jurisdiction: Optional[str] = None
    ) -> List[Regulation]:
        """
        Get all regulations of a specific type.

        Args:
            regulation_type: Type of regulation
            jurisdiction: Optional jurisdiction filter

        Returns:
            List of regulations
        """
        results = []

        for regulation in self.regulations.values():
            if regulation.regulation_type != regulation_type:
                continue
            
            if jurisdiction and regulation.jurisdiction.lower() != jurisdiction.lower():
                continue

            results.append(regulation)

        return results

    def get_latest_version(
        self,
        code: str,
        section: str
    ) -> Optional[Regulation]:
        """
        Get the latest version of a specific regulation.

        Args:
            code: Regulation code (e.g., "IBC")
            section: Section number

        Returns:
            Latest version of the regulation if found
        """
        matching = []

        for regulation in self.regulations.values():
            if code.lower() in regulation.code.lower() and \
               regulation.section == section:
                matching.append(regulation)

        if not matching:
            return None

        # Sort by effective date and return the latest
        matching.sort(key=lambda r: r.effective_date, reverse=True)
        return matching[0]

    def get_all_codes(self) -> List[str]:
        """
        Get list of all unique building codes in database.

        Returns:
            List of code names
        """
        codes = set()
        for regulation in self.regulations.values():
            codes.add(regulation.code)
        return sorted(list(codes))

    def get_all_jurisdictions(self) -> List[str]:
        """
        Get list of all unique jurisdictions in database.

        Returns:
            List of jurisdiction names
        """
        jurisdictions = set()
        for regulation in self.regulations.values():
            jurisdictions.add(regulation.jurisdiction)
        return sorted(list(jurisdictions))

    def update_regulation(
        self,
        regulation_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update an existing regulation.

        Args:
            regulation_id: Regulation ID to update
            updates: Dictionary of fields to update

        Returns:
            True if successful, False if regulation not found
        """
        if regulation_id not in self.regulations:
            return False

        regulation = self.regulations[regulation_id]
        
        # Update allowed fields
        allowed_fields = ["description", "tags", "metadata", "version"]
        for field, value in updates.items():
            if field in allowed_fields and hasattr(regulation, field):
                setattr(regulation, field, value)

        return True

    def delete_regulation(self, regulation_id: str) -> bool:
        """
        Delete a regulation from the database.

        Args:
            regulation_id: Regulation ID to delete

        Returns:
            True if successful, False if regulation not found
        """
        if regulation_id in self.regulations:
            del self.regulations[regulation_id]
            return True
        return False
