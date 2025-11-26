"""Tests for the quest system."""

import pytest
from datetime import datetime, timedelta, timezone
from src.domain.quests import (
    Quest, QuestManager, QuestTemplate, RenewalPolicy,
    QuestCompletion, QuestSnooze
)


class TestQuestCreation:
    """Test quest creation and basic properties."""

    def test_create_quest_from_template(self):
        """Should create quest from template."""
        template = QuestTemplate(
            id="walk_bookstore",
            title="Walk to a bookstore",
            description="Choose any bookstore",
            category="constitutional",
            difficulty="easy",
            base_xp=10,
            optionality="high",
            suggested_locations=[],
            duration_estimate="30 minutes",
            tags=["walk", "literacy"],
            difficulty_factors=None,
            renewal_policy=RenewalPolicy(
                renewal_type="daily",
                cooldown_days=1
            )
        )

        manager = QuestManager()
        quest = manager.create_quest_from_template(template)

        assert quest.title == "Walk to a bookstore"
        assert quest.category == "constitutional"
        assert quest.difficulty == "easy"
        assert quest.xp_reward == 10
        assert quest.status == "active"
        assert quest.template_id == "walk_bookstore"

    def test_create_custom_quest(self):
        """Should create user-defined quest."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="First Friday at SOMArts",
            description="Opening reception",
            category="creative",
            difficulty="easy",
            location="SOMArts Cultural Center",
            xp_reward=20
        )

        assert quest.title == "First Friday at SOMArts"
        assert quest.category == "creative"
        assert quest.xp_reward == 20
        assert quest.status == "active"
        assert quest.template_id is None  # User-created

    def test_quest_with_deadline(self):
        """Should create quest with time constraint."""
        manager = QuestManager()
        due_time = datetime.now(timezone.utc) + timedelta(hours=6)

        quest = manager.create_quest(
            title="Visit SFMOMA",
            category="experiential",
            difficulty="medium",
            xp_reward=15,
            due_at=due_time,
            constraint_type="closing_time",
            constraint_note="Museum closes at 4pm"
        )

        assert quest.due_at is not None
        assert quest.constraint_type == "closing_time"
        assert quest.constraint_note == "Museum closes at 4pm"


class TestQuestCompletion:
    """Test quest completion flow."""

    def test_complete_quest_awards_xp(self):
        """Completing quest should award XP."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Test Quest",
            category="social",
            difficulty="easy",
            xp_reward=15
        )

        result = manager.complete_quest(
            quest.id,
            location_visited="Test Location"
        )

        assert result.xp_awarded == 15
        assert result.quest.status == "completed"
        assert result.quest.completed_at is not None

    def test_complete_quest_with_mood_modifiers(self):
        """Should log additional mood modifiers on completion."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Bike Hawk Hill",
            category="constitutional",
            difficulty="hard",
            xp_reward=30
        )

        result = manager.complete_quest(
            quest.id,
            location_visited="Hawk Hill",
            additional_modifiers=[
                ("beautiful_view", 4),
                ("energized", 8)
            ]
        )

        assert len(result.mood_buffs_applied) >= 3  # Base + category + additionals
        assert any(m[0] == "beautiful_view" for m in result.mood_buffs_applied)
        assert any(m[0] == "energized" for m in result.mood_buffs_applied)

    def test_complete_quest_applies_category_buff(self):
        """Different categories should apply different mood buffs."""
        manager = QuestManager()

        # Constitutional quest
        const_quest = manager.create_quest(
            title="Walk", category="constitutional", difficulty="easy", xp_reward=10
        )
        const_result = manager.complete_quest(const_quest.id)
        const_buff = next(m for m in const_result.mood_buffs_applied if m[0] == "constitutional_activity")
        assert const_buff[1] == 6  # Constitutional = +6

        # Social quest
        social_quest = manager.create_quest(
            title="Coffee", category="social", difficulty="easy", xp_reward=10
        )
        social_result = manager.complete_quest(social_quest.id)
        social_buff = next(m for m in social_result.mood_buffs_applied if m[0] == "social_activity")
        assert social_buff[1] == 8  # Social = +8

    def test_cannot_complete_already_completed_quest(self):
        """Should not be able to complete same quest twice."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Test", category="social", difficulty="easy", xp_reward=10
        )

        # First completion
        manager.complete_quest(quest.id)

        # Second completion should fail
        with pytest.raises(ValueError, match="already completed"):
            manager.complete_quest(quest.id)


class TestQuestRenewal:
    """Test quest renewal system."""

    def test_daily_renewal_sets_pending(self):
        """Daily renewal quest should move to pending_renewal after completion."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Visit Museum",
            category="experiential",
            difficulty="easy",
            xp_reward=10,
            renewal_policy=RenewalPolicy(
                renewal_type="daily",
                cooldown_days=1
            )
        )

        manager.complete_quest(quest.id)
        updated_quest = manager.get_quest(quest.id)

        assert updated_quest.status == "pending_renewal"
        assert updated_quest.next_eligible_renewal is not None

    def test_weekly_renewal_cooldown(self):
        """Weekly renewal should have 7 day cooldown."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Bike Hawk Hill",
            category="constitutional",
            difficulty="hard",
            xp_reward=30,
            renewal_policy=RenewalPolicy(
                renewal_type="weekly",
                cooldown_days=7
            )
        )

        completed_at = datetime.now(timezone.utc)
        manager.complete_quest(quest.id)
        updated_quest = manager.get_quest(quest.id)

        expected_renewal = completed_at + timedelta(days=7)
        # Allow small time difference for test execution
        assert abs((updated_quest.next_eligible_renewal - expected_renewal).total_seconds()) < 5

    def test_seasonal_renewal_respects_active_months(self):
        """Seasonal quest should only renew in active months."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Point Reyes Wildflowers",
            category="experiential",
            difficulty="extreme",
            xp_reward=50,
            renewal_policy=RenewalPolicy(
                renewal_type="seasonal",
                cooldown_days=365,
                active_months=[3, 4, 5]  # March-May
            )
        )

        # Complete in December
        manager.complete_quest(quest.id)

        # Try to renew in December (should not activate)
        manager.process_pending_renewals()
        updated_quest = manager.get_quest(quest.id)
        assert updated_quest.status == "pending_renewal"

        # TODO: Test renewal in spring months

    def test_never_renewal_goes_to_hidden(self):
        """Quest with 'never' renewal should move to hidden."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="One-time Event",
            category="social",
            difficulty="medium",
            xp_reward=15,
            renewal_policy=RenewalPolicy(
                renewal_type="never",
                cooldown_days=0
            )
        )

        manager.complete_quest(quest.id)
        updated_quest = manager.get_quest(quest.id)

        assert updated_quest.status == "hidden"

    def test_renewal_increments_count(self):
        """Renewal should increment renewal_count."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Daily Quest",
            category="constitutional",
            difficulty="easy",
            xp_reward=10,
            renewal_policy=RenewalPolicy(
                renewal_type="daily",
                cooldown_days=1
            )
        )

        assert quest.renewal_count == 0

        # Complete and renew
        manager.complete_quest(quest.id)
        # Simulate time passing
        manager.get_quest(quest.id).next_eligible_renewal = datetime.now(timezone.utc) - timedelta(hours=1)
        manager.process_pending_renewals()

        renewed_quest = manager.get_quest(quest.id)
        assert renewed_quest.renewal_count == 1
        assert renewed_quest.status == "active"


class TestQuestSnooze:
    """Test quest snoozing functionality."""

    def test_snooze_quest_with_reason(self):
        """Should snooze quest with reason."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Bike Ride", category="constitutional", difficulty="medium", xp_reward=15
        )

        snooze = manager.snooze_quest(
            quest.id,
            reason_category="weather",
            reason_text="Too cold and rainy",
            snooze_days=7
        )

        assert snooze.quest_id == quest.id
        assert snooze.reason_category == "weather"
        assert snooze.reason == "Too cold and rainy"

        updated_quest = manager.get_quest(quest.id)
        assert updated_quest.status == "snoozed"

    def test_snooze_without_reason(self):
        """Should allow snoozing without reason."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Test", category="social", difficulty="easy", xp_reward=10
        )

        snooze = manager.snooze_quest(quest.id, snooze_days=7)

        assert snooze.reason is None
        assert snooze.reason_category == "unspecified"

    def test_snooze_auto_return(self):
        """Snoozed quest should auto-return after duration."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Test", category="social", difficulty="easy", xp_reward=10
        )

        # Snooze for 7 days
        manager.snooze_quest(quest.id, snooze_days=7)

        # Simulate time passing (8 days)
        snooze_record = manager.get_snooze_record(quest.id)
        snooze_record.return_at = datetime.now(timezone.utc) - timedelta(hours=1)

        # Process returns
        manager.process_snooze_returns()

        updated_quest = manager.get_quest(quest.id)
        assert updated_quest.status == "active"

    def test_snooze_captures_context(self):
        """Snooze should capture contextual data."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Test", category="constitutional", difficulty="easy", xp_reward=10
        )

        snooze = manager.snooze_quest(
            quest.id,
            reason_category="weather",
            snooze_days=7,
            context={"weather": "Rainy, 45°F", "mood_score": 8}
        )

        assert "weather" in snooze.context
        assert "mood_score" in snooze.context


class TestQuestStates:
    """Test quest state transitions."""

    def test_hide_quest_permanently(self):
        """Should hide quest permanently."""
        manager = QuestManager()
        quest = manager.create_quest(
            title="Unwanted Quest", category="social", difficulty="easy", xp_reward=10
        )

        manager.hide_quest(quest.id)
        updated_quest = manager.get_quest(quest.id)

        assert updated_quest.status == "hidden"

    def test_hidden_quest_not_in_active_list(self):
        """Hidden quests should not appear in active list."""
        manager = QuestManager()
        quest1 = manager.create_quest(
            title="Active", category="social", difficulty="easy", xp_reward=10
        )
        quest2 = manager.create_quest(
            title="Hidden", category="social", difficulty="easy", xp_reward=10
        )

        manager.hide_quest(quest2.id)

        active = manager.get_active_quests()
        assert len(active) == 1
        assert active[0].id == quest1.id


class TestQuestDifficulty:
    """Test difficulty-based XP rewards."""

    def test_difficulty_xp_scaling(self):
        """Different difficulties should have different XP ranges."""
        manager = QuestManager(max_active_quests=10)  # Increase limit for this test

        easy = manager.create_quest(
            title="Easy", category="social", difficulty="easy", xp_reward=10
        )
        medium = manager.create_quest(
            title="Medium", category="social", difficulty="medium", xp_reward=18
        )
        hard = manager.create_quest(
            title="Hard", category="social", difficulty="hard", xp_reward=30
        )
        extreme = manager.create_quest(
            title="Extreme", category="social", difficulty="extreme", xp_reward=50
        )

        assert 5 <= easy.xp_reward <= 10
        assert 15 <= medium.xp_reward <= 20
        assert 25 <= hard.xp_reward <= 35
        assert 40 <= extreme.xp_reward <= 50


class TestQuestHistory:
    """Test quest completion history."""

    def test_get_quest_history(self):
        """Should retrieve quest completion history."""
        manager = QuestManager()
        quest1 = manager.create_quest(
            title="Quest 1", category="social", difficulty="easy", xp_reward=10
        )
        quest2 = manager.create_quest(
            title="Quest 2", category="constitutional", difficulty="easy", xp_reward=10
        )

        manager.complete_quest(quest1.id)
        manager.complete_quest(quest2.id)

        history = manager.get_completion_history(days=7)
        assert len(history) == 2

    def test_quest_stats_by_category(self):
        """Should track completion stats by category."""
        manager = QuestManager()

        # Complete multiple quests
        social = manager.create_quest("Social", "social", "easy", 10)
        const1 = manager.create_quest("Walk 1", "constitutional", "easy", 10)
        const2 = manager.create_quest("Walk 2", "constitutional", "easy", 10)

        manager.complete_quest(social.id)
        manager.complete_quest(const1.id)
        manager.complete_quest(const2.id)

        stats = manager.get_quest_stats()
        assert stats.quests_by_category["social"] == 1
        assert stats.quests_by_category["constitutional"] == 2
        assert stats.total_completed == 3


class TestActiveQuestLimit:
    """Test active quest limit enforcement."""

    def test_respect_max_active_limit(self):
        """Should not exceed max active quest limit."""
        manager = QuestManager(max_active_quests=3)

        # Create 3 quests (at limit)
        q1 = manager.create_quest("Q1", "social", "easy", 10)
        q2 = manager.create_quest("Q2", "social", "easy", 10)
        q3 = manager.create_quest("Q3", "social", "easy", 10)

        # Try to create 4th (should fail or queue)
        with pytest.raises(ValueError, match="maximum.*active quests"):
            q4 = manager.create_quest("Q4", "social", "easy", 10)

    def test_pending_renewal_waits_for_slot(self):
        """Pending renewal should wait if at max active."""
        manager = QuestManager(max_active_quests=2)

        # Create 2 quests and complete one with renewal
        q1 = manager.create_quest(
            "Q1", "social", "easy", 10,
            renewal_policy=RenewalPolicy("daily", 1)
        )
        q2 = manager.create_quest("Q2", "social", "easy", 10)

        manager.complete_quest(q1.id)  # Moves to pending_renewal

        # Try to process renewals (should wait, still at limit)
        manager.process_pending_renewals()

        assert manager.get_quest(q1.id).status == "pending_renewal"
        active = manager.get_active_quests()
        assert len(active) == 1  # Only q2
