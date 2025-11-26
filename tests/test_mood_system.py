"""Tests for the mood calculation system."""

import pytest
from datetime import datetime, timedelta, timezone
from src.domain.mood import MoodCalculator, MoodEvent, MoodModifier, MoodState


class TestMoodCalculation:
    """Test mood score calculation logic."""

    def test_calculate_mood_with_no_events(self):
        """Mood with no events should be 0."""
        calculator = MoodCalculator()
        score = calculator.calculate(events=[], traits=[])
        assert score == 0

    def test_calculate_mood_with_single_positive_event(self):
        """Positive event should increase mood."""
        calculator = MoodCalculator()
        events = [
            MoodEvent(
                id=1,
                event_type="social_interaction",
                modifier=8,
                description="Had coffee with friend",
                created_at=datetime.now(timezone.utc),
                expires_at=None,
                is_active=True
            )
        ]
        score = calculator.calculate(events=events, traits=[])
        assert score == 8

    def test_calculate_mood_with_single_negative_event(self):
        """Negative event should decrease mood."""
        calculator = MoodCalculator()
        events = [
            MoodEvent(
                id=1,
                event_type="ate_without_table",
                modifier=-3,
                description="Ate without table",
                created_at=datetime.now(timezone.utc),
                expires_at=None,
                is_active=True
            )
        ]
        score = calculator.calculate(events=events, traits=[])
        assert score == -3

    def test_calculate_mood_with_multiple_events(self):
        """Multiple events should sum correctly."""
        calculator = MoodCalculator()
        events = [
            MoodEvent(1, "social", 8, "", datetime.now(timezone.utc), None, True),
            MoodEvent(2, "ate_without_table", -3, "", datetime.now(timezone.utc), None, True),
            MoodEvent(3, "fine_meal", 5, "", datetime.now(timezone.utc), None, True),
        ]
        score = calculator.calculate(events=events, traits=[])
        assert score == 10  # 8 - 3 + 5

    def test_calculate_mood_with_traits(self):
        """Traits should affect mood score."""
        from src.domain.traits import Trait

        calculator = MoodCalculator()
        traits = [
            Trait(1, "optimist", "Optimist", 5, True, "rimworld_stock")
        ]
        score = calculator.calculate(events=[], traits=traits)
        assert score == 5

    def test_calculate_mood_with_events_and_traits(self):
        """Events and traits should both contribute."""
        from src.domain.traits import Trait

        calculator = MoodCalculator()
        events = [
            MoodEvent(1, "social", 8, "", datetime.now(timezone.utc), None, True),
        ]
        traits = [
            Trait(1, "optimist", "Optimist", 5, True, "rimworld_stock")
        ]
        score = calculator.calculate(events=events, traits=traits)
        assert score == 13  # 8 + 5

    def test_inactive_events_not_counted(self):
        """Inactive events should not affect mood."""
        calculator = MoodCalculator()
        events = [
            MoodEvent(1, "social", 8, "", datetime.now(timezone.utc), None, True),
            MoodEvent(2, "old_event", 10, "", datetime.now(timezone.utc), None, False),  # inactive
        ]
        score = calculator.calculate(events=events, traits=[])
        assert score == 8  # Only active event counted

    def test_expired_events_not_counted(self):
        """Expired events should not affect mood."""
        calculator = MoodCalculator()
        now = datetime.now(timezone.utc)
        events = [
            MoodEvent(1, "current", 8, "", now, now + timedelta(hours=1), True),
            MoodEvent(2, "expired", 10, "", now - timedelta(days=2), now - timedelta(days=1), True),
        ]
        # Filter out expired events before calculation (this would be done by the engine)
        active_events = [e for e in events if not calculator.is_expired(e)]
        score = calculator.calculate(events=active_events, traits=[])
        assert score == 8


class TestMoodFace:
    """Test mood face/emoji generation."""

    def test_very_happy_face(self):
        """Score >= 20 should be :D"""
        calculator = MoodCalculator()
        face = calculator.get_mood_face(20)
        assert face == ":D"

        face = calculator.get_mood_face(100)
        assert face == ":D"

    def test_happy_face(self):
        """Score 10-19 should be :)"""
        calculator = MoodCalculator()
        face = calculator.get_mood_face(10)
        assert face == ":)"

        face = calculator.get_mood_face(19)
        assert face == ":)"

    def test_neutral_face(self):
        """Score 0-9 should be :|"""
        calculator = MoodCalculator()
        face = calculator.get_mood_face(0)
        assert face == ":|"

        face = calculator.get_mood_face(9)
        assert face == ":|"

    def test_unhappy_face(self):
        """Score -1 to -9 should be :("""
        calculator = MoodCalculator()
        face = calculator.get_mood_face(-1)
        assert face == ":("

        face = calculator.get_mood_face(-9)
        assert face == ":("

    def test_very_unhappy_face(self):
        """Score <= -10 should be D:"""
        calculator = MoodCalculator()
        face = calculator.get_mood_face(-10)
        assert face == "D:"

        face = calculator.get_mood_face(-100)
        assert face == "D:"


class TestMoodState:
    """Test MoodState creation."""

    def test_create_mood_state(self):
        """Should create complete mood state."""
        from src.domain.traits import Trait

        calculator = MoodCalculator()
        events = [
            MoodEvent(1, "social", 8, "", datetime.now(timezone.utc), None, True),
        ]
        traits = [
            Trait(1, "optimist", "Optimist", 5, True, "rimworld_stock")
        ]

        state = calculator.create_mood_state(events=events, traits=traits)

        assert isinstance(state, MoodState)
        assert state.score == 13
        assert state.face == ":)"
        assert len(state.active_events) == 1
        assert len(state.active_traits) == 1
        assert isinstance(state.calculated_at, datetime)


class TestMoodEventExpiration:
    """Test mood event expiration logic."""

    def test_event_without_expiration_never_expires(self):
        """Events with expires_at=None never expire."""
        calculator = MoodCalculator()
        event = MoodEvent(
            1, "permanent", 10, "",
            datetime.now(timezone.utc),
            expires_at=None,
            is_active=True
        )
        assert not calculator.is_expired(event)

    def test_event_expires_after_duration(self):
        """Event should expire after expiration time."""
        calculator = MoodCalculator()
        now = datetime.now(timezone.utc)
        event = MoodEvent(
            1, "temporary", 10, "",
            now - timedelta(hours=25),  # Created 25 hours ago
            expires_at=now - timedelta(hours=1),  # Expired 1 hour ago
            is_active=True
        )
        assert calculator.is_expired(event)

    def test_event_not_yet_expired(self):
        """Event should not expire before expiration time."""
        calculator = MoodCalculator()
        now = datetime.now(timezone.utc)
        event = MoodEvent(
            1, "temporary", 10, "",
            now,
            expires_at=now + timedelta(hours=1),  # Expires in 1 hour
            is_active=True
        )
        assert not calculator.is_expired(event)


class TestMoodModifierLibrary:
    """Test mood modifier library (stock + custom modifiers)."""

    def test_load_stock_modifiers(self):
        """Should load RimWorld stock modifiers."""
        from src.domain.mood import MoodModifierLibrary

        library = MoodModifierLibrary()
        stock = library.get_stock_modifiers()

        assert len(stock) > 0
        assert any(m.event_type == "ate_without_table" for m in stock)
        assert any(m.event_type == "fine_meal" for m in stock)
        assert any(m.event_type == "social_interaction" for m in stock)

    def test_get_modifier_by_type(self):
        """Should retrieve modifier by event_type."""
        from src.domain.mood import MoodModifierLibrary

        library = MoodModifierLibrary()
        modifier = library.get_modifier("ate_without_table")

        assert modifier is not None
        assert modifier.default_value == -3
        assert modifier.name == "Ate without table"

    def test_create_custom_modifier(self):
        """Should allow creating custom modifiers."""
        from src.domain.mood import MoodModifierLibrary

        library = MoodModifierLibrary()
        custom = library.create_custom_modifier(
            event_type="bart_delayed",
            name="BART delayed again",
            default_value=-5,
            duration_hours=2
        )

        assert custom.event_type == "bart_delayed"
        assert custom.default_value == -5
        assert custom.category == "custom"

    def test_custom_modifiers_persist(self):
        """Custom modifiers should be retrievable."""
        from src.domain.mood import MoodModifierLibrary

        library = MoodModifierLibrary()
        library.create_custom_modifier(
            event_type="custom_test",
            name="Custom Test",
            default_value=7
        )

        retrieved = library.get_modifier("custom_test")
        assert retrieved is not None
        assert retrieved.default_value == 7
