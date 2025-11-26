"""User profile and preferences."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class UserProfile:
    """User profile with location and preferences."""

    # Location
    home_address: Optional[str] = None
    home_neighborhood: Optional[str] = None  # e.g., "Inner Richmond"
    home_zipcode: Optional[str] = None  # e.g., "94118"
    home_coordinates: Optional[tuple] = None  # (lat, lon)

    # Memberships (affect difficulty/XP)
    memberships: List[str] = field(default_factory=list)  # e.g., ["Cal Academy", "SFMOMA", "de Young"]

    # Transportation preferences
    has_car: bool = False
    prefers_walking: bool = True
    prefers_transit: bool = True
    prefers_biking: bool = False

    # Distance preferences (in miles)
    easy_distance: float = 0.5  # Within this is "easy"
    medium_distance: float = 2.0  # Within this is "medium"
    hard_distance: float = 5.0  # Within this is "hard", beyond is "extreme"

    # Setup state
    setup_completed: bool = False  # Has user completed first-run setup?

    # Context for LLM
    def get_context_for_llm(self) -> str:
        """Get user context as a string for LLM prompts.

        Note: Does NOT include memberships - those are handled at the application layer
        to avoid the LLM making assumptions about what the user has access to.
        """
        context_parts = []

        if self.home_neighborhood:
            context_parts.append(f"User lives in {self.home_neighborhood}")

        transport = []
        if self.has_car:
            transport.append("car")
        if self.prefers_walking:
            transport.append("walking")
        if self.prefers_transit:
            transport.append("transit")

        if transport:
            context_parts.append(f"Prefers {', '.join(transport)}")

        return ". ".join(context_parts) if context_parts else ""

    def get_difficulty_adjustment(self, location_name: str) -> Dict[str, any]:
        """Calculate difficulty adjustment based on user context.

        Args:
            location_name: Name of the location/venue

        Returns:
            Dictionary with xp_adjustment and reason
        """
        adjustment = {
            "xp_adjustment": 0,
            "xp_multiplier": 1.0,
            "reasons": []
        }

        # Check for membership
        for membership in self.memberships:
            if membership.lower() in location_name.lower():
                adjustment["xp_multiplier"] = 0.7  # Easier if you have membership
                adjustment["xp_adjustment"] = -5
                adjustment["reasons"].append(f"Has {membership} membership")
                break

        return adjustment


# Default profile for SF Inner Richmond resident
DEFAULT_PROFILE = UserProfile(
    home_neighborhood="Inner Richmond",
    home_address=None,  # Not storing actual address
    memberships=[],  # User will add their own
    has_car=False,
    prefers_walking=True,
    prefers_transit=True,
    easy_distance=0.5,
    medium_distance=2.0,
    hard_distance=5.0
)
