"""Mood calculation system for MOOdBBS."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional
from src.domain.traits import Trait


@dataclass
class MoodEvent:
    """A single mood-affecting event."""
    id: int
    event_type: str
    modifier: int
    description: str
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool


@dataclass
class MoodModifier:
    """A mood modifier definition (from library)."""
    event_type: str
    name: str
    default_value: int
    duration_hours: Optional[int]
    category: str  # rimworld_stock, sf_custom, custom


@dataclass
class MoodState:
    """Current mood state."""
    score: int
    face: str  # :D, :), :|, :(, D:
    active_events: List[MoodEvent]
    active_traits: List[Trait]
    calculated_at: datetime


class MoodCalculator:
    """Calculates mood scores from events and traits."""

    def calculate(self, events: List[MoodEvent], traits: List[Trait]) -> int:
        """
        Calculate total mood score.

        Args:
            events: List of active mood events
            traits: List of active traits

        Returns:
            Total mood score (sum of all modifiers)
        """
        score = 0

        # Sum event modifiers
        for event in events:
            if event.is_active:
                score += event.modifier

        # Sum trait modifiers
        for trait in traits:
            if trait.is_active:
                score += trait.mood_modifier

        return score

    def get_mood_face(self, score: int) -> str:
        """
        Get mood face emoji based on score.

        Args:
            score: Current mood score

        Returns:
            Mood face string
        """
        if score >= 16:
            return ":D"      # Very happy (16+)
        elif score >= 6:
            return ":)"      # Happy (6-15)
        elif score >= -5:
            return ":|"      # Neutral (-5 to 5)
        elif score >= -15:
            return ":("      # Unhappy (-15 to -6)
        else:
            return "D:"      # Very unhappy (-16 or lower)

    def is_expired(self, event: MoodEvent) -> bool:
        """
        Check if an event has expired.

        Args:
            event: Mood event to check

        Returns:
            True if expired, False otherwise
        """
        if event.expires_at is None:
            return False

        return datetime.now(timezone.utc) > event.expires_at

    def create_mood_state(
        self,
        events: List[MoodEvent],
        traits: List[Trait]
    ) -> MoodState:
        """
        Create a complete mood state snapshot.

        Args:
            events: Active mood events
            traits: Active traits

        Returns:
            Complete MoodState object
        """
        score = self.calculate(events, traits)
        face = self.get_mood_face(score)

        return MoodState(
            score=score,
            face=face,
            active_events=events,
            active_traits=traits,
            calculated_at=datetime.now(timezone.utc)
        )


class MoodModifierLibrary:
    """Library of stock and custom mood modifiers."""

    # Stock RimWorld modifiers
    STOCK_MODIFIERS = [
        MoodModifier("ate_without_table", "Ate without table", -3, 24, "rimworld_stock"),
        MoodModifier("fine_meal", "Had a fine meal", 5, 24, "rimworld_stock"),
        MoodModifier("social_interaction", "Social interaction", 8, 24, "rimworld_stock"),
        MoodModifier("completed_walk", "Completed a walk", 6, 24, "rimworld_stock"),
        MoodModifier("too_long_indoors", "Too long indoors", -5, 24, "rimworld_stock"),
        MoodModifier("saw_beauty", "Saw something beautiful", 4, 12, "rimworld_stock"),
    ]

    def __init__(self):
        """Initialize the modifier library."""
        self.custom_modifiers: List[MoodModifier] = []

    def get_stock_modifiers(self) -> List[MoodModifier]:
        """Get all stock RimWorld modifiers."""
        return self.STOCK_MODIFIERS.copy()

    def get_modifier(self, event_type: str) -> Optional[MoodModifier]:
        """
        Get a modifier by event type.

        Args:
            event_type: Event type to look up

        Returns:
            MoodModifier if found, None otherwise
        """
        # Check stock modifiers first
        for modifier in self.STOCK_MODIFIERS:
            if modifier.event_type == event_type:
                return modifier

        # Check custom modifiers
        for modifier in self.custom_modifiers:
            if modifier.event_type == event_type:
                return modifier

        return None

    def create_custom_modifier(
        self,
        event_type: str,
        name: str,
        default_value: int,
        duration_hours: Optional[int] = None
    ) -> MoodModifier:
        """
        Create a new custom mood modifier.

        Args:
            event_type: Unique identifier for the event type
            name: Display name
            default_value: Default mood modifier value
            duration_hours: How long the modifier lasts

        Returns:
            Created MoodModifier
        """
        modifier = MoodModifier(
            event_type=event_type,
            name=name,
            default_value=default_value,
            duration_hours=duration_hours,
            category="custom"
        )

        self.custom_modifiers.append(modifier)
        return modifier
