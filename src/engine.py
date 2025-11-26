"""MOOdBBS Game Engine - integrates all game systems."""

from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict, Any

from src.domain.mood import MoodCalculator, MoodEvent, MoodState, MoodModifierLibrary
from src.domain.quests import QuestManager, Quest, QuestCompletionResult, QuestStats
from src.domain.traits import Trait
from src.database.db import Database


class MOOdBBSEngine:
    """
    The core game engine for MOOdBBS.

    This is the single source of truth for all game state.
    All frontends (shell, TUI, API) interact through this interface.
    """

    def __init__(self, max_active_quests: int = 3, db_path: str = "data/moodbbs.db"):
        """Initialize the game engine.

        Args:
            max_active_quests: Maximum number of active quests
            db_path: Path to SQLite database
        """
        self.db = Database(db_path)
        self.mood_calculator = MoodCalculator()
        self.mood_library = MoodModifierLibrary()
        self.quest_manager = QuestManager(max_active_quests=max_active_quests)

        # Load data from database
        self._load_from_database()

    def _load_from_database(self):
        """Load all data from database into memory."""
        # Load quests
        quests = self.db.load_quests()
        for quest in quests:
            self.quest_manager._quests[quest.id] = quest
        if quests:
            self.quest_manager._next_quest_id = max(q.id for q in quests) + 1
        else:
            self.quest_manager._next_quest_id = 1

        # Load quest completions
        completions = self.db.load_quest_completions()
        for completion in completions:
            self.quest_manager._completions[completion.id] = completion
        if completions:
            self.quest_manager._next_completion_id = max(c.id for c in completions) + 1
        else:
            self.quest_manager._next_completion_id = 1

        # Load mood events
        self._mood_events = self.db.load_mood_events()
        if self._mood_events:
            self._next_event_id = max(e.id for e in self._mood_events) + 1
        else:
            self._next_event_id = 1

        # Load traits
        self._traits = self.db.load_traits()
        if self._traits:
            self._next_trait_id = max(t.id for t in self._traits) + 1
        else:
            self._next_trait_id = 1

        # Load total XP
        self.quest_manager._total_xp = self.db.get_total_xp()

    # ==================== Mood System ====================

    def get_current_mood(self) -> MoodState:
        """Get current mood score and contributing factors."""
        active_events = [e for e in self._mood_events if e.is_active]

        # Filter out expired events
        active_events = [
            e for e in active_events
            if not self.mood_calculator.is_expired(e)
        ]

        active_traits = [t for t in self._traits if t.is_active]

        return self.mood_calculator.create_mood_state(
            events=active_events,
            traits=active_traits
        )

    def log_mood_event(
        self,
        event_type: str,
        modifier: int,
        description: str = "",
        duration_hours: Optional[int] = None
    ) -> MoodEvent:
        """Log a new mood-affecting event.

        Args:
            event_type: Type of event (e.g., 'ate_without_table')
            modifier: Mood modifier value
            description: Optional description
            duration_hours: How long the modifier lasts (None = permanent)

        Returns:
            Created MoodEvent
        """
        from datetime import timedelta

        now = datetime.now(timezone.utc)
        expires_at = None
        if duration_hours:
            expires_at = now + timedelta(hours=duration_hours)

        event = MoodEvent(
            id=self._next_event_id,
            event_type=event_type,
            modifier=modifier,
            description=description,
            created_at=now,
            expires_at=expires_at,
            is_active=True
        )

        self._mood_events.append(event)
        self._next_event_id += 1

        # Save to database
        self.db.save_mood_event(event)

        return event

    def get_active_mood_events(self) -> List[MoodEvent]:
        """Get all currently active mood modifiers."""
        active = [e for e in self._mood_events if e.is_active]

        # Filter out expired
        active = [
            e for e in active
            if not self.mood_calculator.is_expired(e)
        ]

        return active

    def get_mood_modifier_library(self) -> List:
        """Get available mood modifiers (stock + custom)."""
        return self.mood_library.get_stock_modifiers()

    def create_custom_modifier(
        self,
        event_type: str,
        name: str,
        default_value: int,
        category: str = "custom"
    ):
        """Create a new custom mood modifier.

        Args:
            event_type: Unique event type identifier
            name: Display name
            default_value: Default modifier value
            category: Category (default: "custom")

        Returns:
            Created MoodModifier
        """
        return self.mood_library.create_custom_modifier(
            event_type=event_type,
            name=name,
            default_value=default_value
        )

    # ==================== Quest System ====================

    def get_active_quests(self, limit: int = 10, filter_by_eligibility: bool = True) -> List[Quest]:
        """Get active quests.

        Args:
            limit: Maximum number to return
            filter_by_eligibility: If True, only return quests eligible today

        Returns:
            List of active quests
        """
        return self.quest_manager.get_active_quests(limit=limit, filter_by_eligibility=filter_by_eligibility)

    def get_quest_by_id(self, quest_id: int) -> Quest:
        """Get a specific quest.

        Args:
            quest_id: Quest ID

        Returns:
            Quest instance

        Raises:
            ValueError: If quest not found
        """
        return self.quest_manager.get_quest(quest_id)

    def create_quest(
        self,
        title: str,
        description: str = "",
        category: str = "experiential",
        difficulty: str = "easy",
        location: str = "",
        xp_reward: int = 10,
        due_hours: Optional[int] = None,
        renewal_policy: Optional[Any] = None,
        constraint_type: Optional[str] = None,
        constraint_note: Optional[str] = None
    ) -> Quest:
        """Create a new quest.

        Args:
            title: Quest title
            description: Quest description
            category: Quest category
            difficulty: Difficulty level
            location: Location
            xp_reward: XP reward
            due_hours: Hours until deadline
            renewal_policy: Optional renewal policy
            constraint_type: Type of time constraint (day_of_week, day_of_month)
            constraint_note: Constraint details (e.g., "Friday", "first_friday")

        Returns:
            Created Quest
        """
        from datetime import timedelta

        due_at = None
        if due_hours:
            due_at = datetime.now(timezone.utc) + timedelta(hours=due_hours)

        quest = self.quest_manager.create_quest(
            title=title,
            description=description,
            category=category,
            difficulty=difficulty,
            location=location,
            xp_reward=xp_reward,
            due_at=due_at,
            renewal_policy=renewal_policy,
            constraint_type=constraint_type,
            constraint_note=constraint_note
        )

        # Save to database
        self.db.save_quest(quest)

        return quest

    def complete_quest(
        self,
        quest_id: int,
        notes: str = "",
        additional_modifiers: Optional[List[Tuple[str, int]]] = None
    ) -> QuestCompletionResult:
        """Complete a quest.

        Args:
            quest_id: ID of quest to complete
            notes: Optional notes
            additional_modifiers: Additional mood modifiers to log

        Returns:
            QuestCompletionResult with XP and mood buffs
        """
        result = self.quest_manager.complete_quest(
            quest_id=quest_id,
            notes=notes,
            additional_modifiers=additional_modifiers
        )

        # Apply mood buffs to engine
        for event_type, modifier in result.mood_buffs_applied:
            self.log_mood_event(
                event_type=event_type,
                modifier=modifier,
                description=f"Quest completion: {result.quest.title}",
                duration_hours=24
            )

        # Save quest and completion to database
        self.db.save_quest(result.quest)
        # Find the completion record that was just created
        completion = max(self.quest_manager._completions.values(), key=lambda c: c.completed_at)
        self.db.save_quest_completion(completion)
        self.db.set_total_xp(result.total_xp)

        return result

    def snooze_quest(
        self,
        quest_id: int,
        reason_category: str = "unspecified",
        reason_text: Optional[str] = None,
        snooze_days: int = 7
    ):
        """Snooze a quest.

        Args:
            quest_id: Quest to snooze
            reason_category: Reason category
            reason_text: Optional reason text
            snooze_days: Days to snooze
        """
        # Get current mood for context
        mood = self.get_current_mood()

        context = {
            "mood_score": mood.score,
            "day_of_week": datetime.now().strftime("%A")
        }

        result = self.quest_manager.snooze_quest(
            quest_id=quest_id,
            reason_category=reason_category,
            reason_text=reason_text,
            snooze_days=snooze_days,
            context=context
        )

        # Save updated quest to database
        quest = self.quest_manager.get_quest(quest_id)
        self.db.save_quest(quest)

        return result

    def hide_quest(self, quest_id: int):
        """Hide a quest permanently.

        Args:
            quest_id: Quest to hide
        """
        self.quest_manager.hide_quest(quest_id)

        # Save updated quest to database
        quest = self.quest_manager.get_quest(quest_id)
        self.db.save_quest(quest)

    def get_quest_history(self, days: int = 7):
        """Get recently completed quests.

        Args:
            days: Days to look back

        Returns:
            List of QuestCompletion records
        """
        return self.quest_manager.get_completion_history(days=days)

    def get_quest_stats(self) -> QuestStats:
        """Get quest statistics."""
        return self.quest_manager.get_quest_stats()

    # ==================== Trait System ====================

    def get_active_traits(self) -> List[Trait]:
        """Get user's active traits."""
        return [t for t in self._traits if t.is_active]

    def add_trait(
        self,
        trait_name: str,
        description: str = "",
        mood_modifier: int = 0
    ) -> Trait:
        """Add a trait to the user.

        Args:
            trait_name: Name of trait
            description: Description
            mood_modifier: Mood modifier value

        Returns:
            Created Trait
        """
        trait = Trait(
            id=self._next_trait_id,
            trait_name=trait_name,
            description=description,
            mood_modifier=mood_modifier,
            is_active=True,
            category="custom"
        )

        self._traits.append(trait)
        self._next_trait_id += 1

        # Save to database
        self.db.save_trait(trait)

        return trait

    def remove_trait(self, trait_name: str) -> bool:
        """Remove a trait from the user.

        Args:
            trait_name: Name of trait to remove

        Returns:
            True if removed, False if not found
        """
        for trait in self._traits:
            if trait.trait_name == trait_name:
                trait.is_active = False
                # Save to database
                self.db.save_trait(trait)
                return True
        return False

    # ==================== User Stats ====================

    def get_user_stats(self) -> Dict[str, Any]:
        """Get overall user statistics."""
        quest_stats = self.get_quest_stats()
        mood = self.get_current_mood()

        return {
            "total_xp": quest_stats.total_xp_earned,
            "quests_completed": quest_stats.total_completed,
            "current_mood": mood.score,
            "active_traits": len(self.get_active_traits()),
            "active_modifiers": len(self.get_active_mood_events())
        }
