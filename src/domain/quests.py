"""Quest system for MOOdBBS."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Tuple, Any
from enum import Enum


@dataclass
class RenewalPolicy:
    """Defines when/how a quest renews."""
    renewal_type: str  # daily, weekly, monthly, seasonal, never
    cooldown_days: int  # Minimum days before renewal
    max_active_instances: int = 1  # How many can be active at once
    active_months: Optional[List[int]] = None  # For seasonal [3,4,5]
    schedule: Optional[str] = None  # "first_friday", etc.


@dataclass
class QuestTemplate:
    """Reusable quest pattern."""
    id: str
    title: str
    description: str
    category: str  # social, constitutional, creative, experiential
    difficulty: str  # easy, medium, hard, extreme
    base_xp: int
    optionality: str  # high, medium, low
    suggested_locations: List[Dict]
    duration_estimate: str
    tags: List[str]
    difficulty_factors: Optional[Dict] = None
    renewal_policy: Optional[RenewalPolicy] = None


@dataclass
class Quest:
    """Active quest instance."""
    id: int
    template_id: Optional[str]
    title: str
    description: str
    category: str
    difficulty: str
    location: str
    xp_reward: int
    status: str  # active, snoozed, completed, pending_renewal, hidden
    renewal_policy: Optional[RenewalPolicy]
    next_eligible_renewal: Optional[datetime]
    renewal_count: int
    created_at: datetime
    due_at: Optional[datetime] = None
    constraint_type: Optional[str] = None
    constraint_note: Optional[str] = None
    completed_at: Optional[datetime] = None


@dataclass
class QuestCompletion:
    """Completion record."""
    id: int
    quest_id: int
    completed_at: datetime
    location_visited: str
    duration_minutes: Optional[int]
    notes: str
    mood_modifiers_logged: List[Tuple[str, int]]
    xp_awarded: int


@dataclass
class QuestCompletionResult:
    """Result of completing a quest."""
    quest: Quest
    xp_awarded: int
    mood_buffs_applied: List[Tuple[str, int]]
    total_xp: int


@dataclass
class QuestSnooze:
    """Record of why/when a quest was snoozed."""
    id: int
    quest_id: int
    snoozed_at: datetime
    return_at: datetime
    reason: Optional[str]  # Actual reason text
    reason_category: str  # weather, time, mood, other, unspecified
    context: Dict[str, Any]


@dataclass
class QuestStats:
    """Quest statistics."""
    total_completed: int
    quests_by_category: Dict[str, int]
    total_xp_earned: int
    avg_completion_time: Optional[float]


class QuestManager:
    """Manages quest lifecycle and operations."""

    # Category-specific mood buffs
    CATEGORY_MOOD_BUFFS = {
        "constitutional": ("constitutional_activity", 6),
        "social": ("social_activity", 8),
        "creative": ("creative_activity", 5),
        "experiential": ("experiential_activity", 7)
    }

    def __init__(self, max_active_quests: int = 3):
        """Initialize quest manager.

        Args:
            max_active_quests: Maximum number of active quests allowed
        """
        self.max_active_quests = max_active_quests
        self._quests: Dict[int, Quest] = {}
        self._completions: Dict[int, QuestCompletion] = {}
        self._snoozes: Dict[int, QuestSnooze] = {}
        self._next_quest_id = 1
        self._next_completion_id = 1
        self._next_snooze_id = 1
        self._total_xp = 0

    def create_quest_from_template(self, template: QuestTemplate) -> Quest:
        """Create quest instance from template.

        Args:
            template: Quest template to instantiate

        Returns:
            Created Quest instance
        """
        quest = Quest(
            id=self._next_quest_id,
            template_id=template.id,
            title=template.title,
            description=template.description,
            category=template.category,
            difficulty=template.difficulty,
            location="",
            xp_reward=template.base_xp,
            status="active",
            renewal_policy=template.renewal_policy,
            next_eligible_renewal=None,
            renewal_count=0,
            created_at=datetime.now(timezone.utc)
        )

        self._quests[quest.id] = quest
        self._next_quest_id += 1

        return quest

    def create_quest(
        self,
        title: str,
        category: str,
        difficulty: str,
        xp_reward: int,
        description: str = "",
        location: str = "",
        due_at: Optional[datetime] = None,
        constraint_type: Optional[str] = None,
        constraint_note: Optional[str] = None,
        renewal_policy: Optional[RenewalPolicy] = None
    ) -> Quest:
        """Create a custom quest.

        Args:
            title: Quest title
            category: Quest category
            difficulty: Quest difficulty level
            xp_reward: XP awarded on completion
            description: Optional description
            location: Optional location
            due_at: Optional deadline
            constraint_type: Optional constraint type
            constraint_note: Optional constraint note
            renewal_policy: Optional renewal policy

        Returns:
            Created Quest instance

        Raises:
            ValueError: If at max active quest limit
        """
        # Check active quest limit
        active_count = len(self.get_active_quests())
        if active_count >= self.max_active_quests:
            raise ValueError(f"Already at maximum of {self.max_active_quests} active quests")

        quest = Quest(
            id=self._next_quest_id,
            template_id=None,  # User-created
            title=title,
            description=description,
            category=category,
            difficulty=difficulty,
            location=location,
            xp_reward=xp_reward,
            status="active",
            renewal_policy=renewal_policy,
            next_eligible_renewal=None,
            renewal_count=0,
            created_at=datetime.now(timezone.utc),
            due_at=due_at,
            constraint_type=constraint_type,
            constraint_note=constraint_note
        )

        self._quests[quest.id] = quest
        self._next_quest_id += 1

        return quest

    def complete_quest(
        self,
        quest_id: int,
        location_visited: str = "",
        notes: str = "",
        additional_modifiers: Optional[List[Tuple[str, int]]] = None
    ) -> QuestCompletionResult:
        """Complete a quest.

        Args:
            quest_id: ID of quest to complete
            location_visited: Where user went
            notes: Optional notes
            additional_modifiers: Additional mood modifiers to log

        Returns:
            QuestCompletionResult with XP and mood buffs

        Raises:
            ValueError: If quest not found or already completed
        """
        if quest_id not in self._quests:
            raise ValueError(f"Quest {quest_id} not found")

        quest = self._quests[quest_id]

        if quest.status == "completed":
            raise ValueError(f"Quest {quest_id} already completed")

        # Mark quest as completed
        quest.completed_at = datetime.now(timezone.utc)

        # Award XP
        xp_awarded = quest.xp_reward
        self._total_xp += xp_awarded

        # Build mood buffs list
        mood_buffs = []

        # Base quest completion buff
        mood_buffs.append(("quest_completed", 5))

        # Category-specific buff
        if quest.category in self.CATEGORY_MOOD_BUFFS:
            category_buff = self.CATEGORY_MOOD_BUFFS[quest.category]
            mood_buffs.append(category_buff)

        # Additional modifiers
        if additional_modifiers:
            mood_buffs.extend(additional_modifiers)

        # Create completion record
        completion = QuestCompletion(
            id=self._next_completion_id,
            quest_id=quest_id,
            completed_at=quest.completed_at,
            location_visited=location_visited,
            duration_minutes=None,
            notes=notes,
            mood_modifiers_logged=mood_buffs,
            xp_awarded=xp_awarded
        )

        self._completions[completion.id] = completion
        self._next_completion_id += 1

        # Handle renewal
        if quest.renewal_policy:
            self._handle_quest_renewal(quest)
        else:
            quest.status = "completed"

        return QuestCompletionResult(
            quest=quest,
            xp_awarded=xp_awarded,
            mood_buffs_applied=mood_buffs,
            total_xp=self._total_xp
        )

    def _handle_quest_renewal(self, quest: Quest):
        """Handle quest renewal after completion.

        Args:
            quest: Quest to renew
        """
        policy = quest.renewal_policy

        if policy.renewal_type == "never":
            quest.status = "hidden"
            return

        # Calculate next eligible renewal date
        next_renewal = datetime.now(timezone.utc) + timedelta(days=policy.cooldown_days)
        quest.next_eligible_renewal = next_renewal
        quest.status = "pending_renewal"

    def process_pending_renewals(self):
        """Process quests waiting for renewal.

        Checks all pending_renewal quests and activates those whose
        cooldown has elapsed and seasonal restrictions allow.
        """
        now = datetime.now(timezone.utc)
        current_month = now.month

        for quest in self._quests.values():
            if quest.status != "pending_renewal":
                continue

            if quest.next_eligible_renewal is None:
                continue

            # Check if cooldown elapsed
            if quest.next_eligible_renewal > now:
                continue

            # Check seasonal restrictions
            if quest.renewal_policy and quest.renewal_policy.active_months:
                if current_month not in quest.renewal_policy.active_months:
                    continue  # Wait for right season

            # Check if room in active quests
            active_count = len(self.get_active_quests())
            if active_count >= self.max_active_quests:
                continue  # Wait for slot

            # Renew quest
            quest.status = "active"
            quest.renewal_count += 1
            quest.next_eligible_renewal = None
            quest.completed_at = None

    def snooze_quest(
        self,
        quest_id: int,
        reason_category: str = "unspecified",
        reason_text: Optional[str] = None,
        snooze_days: int = 7,
        context: Optional[Dict[str, Any]] = None
    ) -> QuestSnooze:
        """Snooze a quest.

        Args:
            quest_id: ID of quest to snooze
            reason_category: Category of reason (weather, time, mood, other, unspecified)
            reason_text: Optional text explanation
            snooze_days: Days to snooze for
            context: Optional context data (weather, mood, etc.)

        Returns:
            QuestSnooze record

        Raises:
            ValueError: If quest not found
        """
        if quest_id not in self._quests:
            raise ValueError(f"Quest {quest_id} not found")

        quest = self._quests[quest_id]
        quest.status = "snoozed"

        now = datetime.now(timezone.utc)
        return_at = now + timedelta(days=snooze_days)

        snooze = QuestSnooze(
            id=self._next_snooze_id,
            quest_id=quest_id,
            snoozed_at=now,
            return_at=return_at,
            reason=reason_text,
            reason_category=reason_category,
            context=context or {}
        )

        self._snoozes[snooze.id] = snooze
        self._next_snooze_id += 1

        return snooze

    def get_snooze_record(self, quest_id: int) -> Optional[QuestSnooze]:
        """Get snooze record for a quest.

        Args:
            quest_id: Quest ID

        Returns:
            Most recent QuestSnooze for this quest, or None
        """
        # Find most recent snooze for this quest
        snoozes = [s for s in self._snoozes.values() if s.quest_id == quest_id]
        if not snoozes:
            return None

        return max(snoozes, key=lambda s: s.snoozed_at)

    def process_snooze_returns(self):
        """Process snoozed quests and return them to active if time elapsed."""
        now = datetime.now(timezone.utc)

        for snooze in self._snoozes.values():
            if snooze.return_at > now:
                continue

            if snooze.quest_id not in self._quests:
                continue

            quest = self._quests[snooze.quest_id]
            if quest.status == "snoozed":
                quest.status = "active"

    def hide_quest(self, quest_id: int):
        """Hide a quest permanently.

        Args:
            quest_id: ID of quest to hide

        Raises:
            ValueError: If quest not found
        """
        if quest_id not in self._quests:
            raise ValueError(f"Quest {quest_id} not found")

        quest = self._quests[quest_id]
        quest.status = "hidden"

    def get_quest(self, quest_id: int) -> Quest:
        """Get a quest by ID.

        Args:
            quest_id: Quest ID

        Returns:
            Quest instance

        Raises:
            ValueError: If quest not found
        """
        if quest_id not in self._quests:
            raise ValueError(f"Quest {quest_id} not found")

        return self._quests[quest_id]

    def is_quest_eligible_today(self, quest: Quest) -> bool:
        """Check if a quest is eligible to be shown today based on time constraints.

        Args:
            quest: Quest to check

        Returns:
            True if quest should be shown today, False otherwise
        """
        if not quest.constraint_type or not quest.constraint_note:
            return True  # No constraints means always eligible

        now = datetime.now(timezone.utc)

        if quest.constraint_type == "day_of_week":
            # Check day of week (e.g., "Friday", "Mon,Wed,Fri")
            today = now.strftime("%A")  # Full day name
            allowed_days = [d.strip() for d in quest.constraint_note.split(",")]

            # Support both full names and abbreviations
            for day in allowed_days:
                if day.lower() in today.lower() or today.lower().startswith(day.lower()[:3]):
                    return True
            return False

        elif quest.constraint_type == "day_of_month":
            # Handle special patterns like "first_friday"
            note = quest.constraint_note.lower()

            if "_" in note:
                # Pattern like "first_friday", "last_saturday"
                parts = note.split("_")
                if len(parts) == 2:
                    position, day_name = parts

                    # Check if today matches the day name
                    today_name = now.strftime("%A").lower()
                    if not today_name.startswith(day_name[:3]):
                        return False

                    # Check if it's the right week of the month
                    day_of_month = now.day

                    if position == "first":
                        return 1 <= day_of_month <= 7
                    elif position == "second":
                        return 8 <= day_of_month <= 14
                    elif position == "third":
                        return 15 <= day_of_month <= 21
                    elif position == "fourth":
                        return 22 <= day_of_month <= 28
                    elif position == "last":
                        # Last occurrence - check if this is the last instance this month
                        import calendar
                        last_day = calendar.monthrange(now.year, now.month)[1]
                        return day_of_month > last_day - 7

            else:
                # Simple day numbers (e.g., "1", "15", "1,15")
                allowed_days = [int(d.strip()) for d in quest.constraint_note.split(",")]
                return now.day in allowed_days

        return True

    def get_active_quests(self, limit: int = 10, filter_by_eligibility: bool = True) -> List[Quest]:
        """Get active quests.

        Args:
            limit: Maximum number to return
            filter_by_eligibility: If True, only return quests eligible today

        Returns:
            List of active quests
        """
        active = [
            q for q in self._quests.values()
            if q.status == "active"
        ]

        # Filter by time eligibility if requested
        if filter_by_eligibility:
            active = [q for q in active if self.is_quest_eligible_today(q)]

        # Sort by created_at
        active.sort(key=lambda q: q.created_at)

        return active[:limit]

    def get_completion_history(self, days: int = 7) -> List[QuestCompletion]:
        """Get quest completion history.

        Args:
            days: Number of days to look back

        Returns:
            List of QuestCompletion records
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        history = [
            c for c in self._completions.values()
            if c.completed_at >= cutoff
        ]

        # Sort by completion time, most recent first
        history.sort(key=lambda c: c.completed_at, reverse=True)

        return history

    def get_quest_stats(self) -> QuestStats:
        """Get quest statistics.

        Returns:
            QuestStats with completion counts and XP
        """
        completed_quests = [
            self._quests[c.quest_id]
            for c in self._completions.values()
            if c.quest_id in self._quests
        ]

        # Count by category
        by_category: Dict[str, int] = {}
        for quest in completed_quests:
            category = quest.category
            by_category[category] = by_category.get(category, 0) + 1

        return QuestStats(
            total_completed=len(self._completions),
            quests_by_category=by_category,
            total_xp_earned=self._total_xp,
            avg_completion_time=None
        )
