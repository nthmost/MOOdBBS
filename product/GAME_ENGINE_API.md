# MOOdBBS Game Engine API Design

## Philosophy

The MOOdBBS game engine is a **headless core** that manages all game state, business logic, and persistence. It exposes a clean API that any frontend can use - Rich TUI, command shell, HTTP API, or future interfaces.

**Key Principle:** Any interaction with the game state MUST go through the engine API. No frontend should touch the database directly.

## Core Game Engine Interface

```python
class MOOdBBSEngine:
    """
    The core game engine for MOOdBBS.

    This is the single source of truth for all game state.
    All frontends interact with the game through this API.
    """

    # ==================== Mood System ====================

    def get_current_mood(self) -> MoodState:
        """Get current mood score and contributing factors."""

    def log_mood_event(
        self,
        event_type: str,
        modifier: int,
        description: str = "",
        duration_hours: Optional[int] = None
    ) -> MoodEvent:
        """Log a new mood-affecting event."""

    def get_active_mood_events(self) -> List[MoodEvent]:
        """Get all currently active mood modifiers."""

    def get_mood_history(
        self,
        hours: int = 24
    ) -> List[MoodSnapshot]:
        """Get historical mood data."""

    def get_mood_modifier_library(self) -> List[MoodModifier]:
        """Get available mood modifiers (stock + custom)."""

    def create_custom_modifier(
        self,
        event_type: str,
        name: str,
        default_value: int,
        category: str = "custom"
    ) -> MoodModifier:
        """Create a new custom mood modifier."""

    # ==================== Quest System ====================

    def get_active_quests(self, limit: int = 10) -> List[Quest]:
        """Get active quests."""

    def get_quest_by_id(self, quest_id: int) -> Optional[Quest]:
        """Get a specific quest."""

    def create_quest(
        self,
        title: str,
        description: str = "",
        category: str = "experiential",
        location: str = "",
        xp_reward: int = 10,
        due_hours: Optional[int] = None
    ) -> Quest:
        """Create a new quest."""

    def complete_quest(
        self,
        quest_id: int,
        notes: str = "",
        additional_modifiers: Optional[List[Tuple[str, int]]] = None
    ) -> QuestCompletionResult:
        """
        Complete a quest.

        Returns result with XP awarded, mood buffs applied, etc.
        Optionally log additional mood modifiers (pain, energized, etc.)
        """

    def get_quest_history(
        self,
        days: int = 7
    ) -> List[QuestCompletion]:
        """Get recently completed quests."""

    def get_quest_stats(self) -> QuestStats:
        """Get quest statistics (completions by category, etc.)."""

    # ==================== Trait System ====================

    def get_active_traits(self) -> List[Trait]:
        """Get user's active traits."""

    def add_trait(self, trait_name: str) -> Trait:
        """Add a trait to the user."""

    def remove_trait(self, trait_name: str) -> bool:
        """Remove a trait from the user."""

    def get_available_traits(self) -> List[Trait]:
        """Get all available traits (stock library)."""

    # ==================== User Profile ====================

    def get_user_stats(self) -> UserStats:
        """Get overall user statistics (total XP, quests completed, etc.)."""

    def get_settings(self) -> Dict[str, Any]:
        """Get user settings."""

    def update_setting(self, key: str, value: Any) -> None:
        """Update a user setting."""

    # ==================== System ====================

    def take_snapshot(self) -> None:
        """Save current mood state as snapshot."""

    def get_last_login(self) -> Optional[datetime]:
        """Get last login timestamp."""

    def update_last_login(self) -> None:
        """Update last login to now."""
```

## Data Models

### Core Domain Models

```python
@dataclass
class MoodState:
    """Current mood state."""
    score: int
    face: str  # :D, :), :|, :(, D:
    active_events: List[MoodEvent]
    active_traits: List[Trait]
    calculated_at: datetime

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
    category: str  # rimworld_stock, sf_custom, user_custom

@dataclass
class Quest:
    """A quest."""
    id: int
    title: str
    description: str
    category: str  # social, constitutional, creative, experiential
    location: str
    xp_reward: int
    status: str  # active, completed, expired, hidden
    created_at: datetime
    due_at: Optional[datetime]
    completed_at: Optional[datetime]

@dataclass
class QuestCompletionResult:
    """Result of completing a quest."""
    quest: Quest
    xp_awarded: int
    mood_buffs_applied: List[MoodEvent]
    total_xp: int  # User's total XP after completion

@dataclass
class Trait:
    """A personality trait."""
    id: int
    trait_name: str
    description: str
    mood_modifier: int
    is_active: bool
    category: str  # rimworld_stock, custom

@dataclass
class UserStats:
    """Overall user statistics."""
    total_xp: int
    quests_completed: int
    quests_by_category: Dict[str, int]
    current_mood: int
    average_mood_7d: float
    days_tracking: int
    last_login: Optional[datetime]
```

## Command Shell Interface

The shell provides a REPL for interacting with the game engine:

```bash
$ python -m moodbbs.shell

MOOdBBS Shell v0.1.0
Type 'help' for commands, 'exit' to quit

moodbbs> mood
Current Mood: :) [+12]

Active Modifiers:
  +10  started_moodbbs - Started using MOOdBBS!
  +5   optimist - Optimist trait
  -3   ate_without_table - Ate without table

moodbbs> quests
Active Quests:
  1. Visit Coit Tower before sunset [15 XP]
  2. Get coffee at a new cafe [10 XP]
  3. Walk to the ocean [20 XP]

moodbbs> complete 1
Quest completed! +15 XP
Log additional mood modifiers? (y/n): y

Available modifiers:
  1. Pain (-1 to -10)
  2. Energized (+1 to +10)
  3. Beautiful view (+4)
  4. Custom...

Select (or 'done'): 3
Added: Beautiful view (+4)

Select (or 'done'): done

Total XP: 15
Mood updated: :) [+12] → :) [+16]

moodbbs> log ate_without_table
Logged: Ate without table (-3)
Mood updated: :) [+16] → :) [+13]

moodbbs> log --custom "BART delayed" -5
Logged: BART delayed (-5)
Mood updated: :) [+13] → :| [+8]

moodbbs> history mood --hours 24
Mood History (last 24 hours):
  12:00  +12  :)
  13:30  +16  :)
  14:15  +13  :)
  14:20  +8   :|

moodbbs> traits
Active Traits:
  • Optimist (+5)

moodbbs> help

Available commands:
  mood                    - Show current mood
  mood history            - Show mood history
  log <event>             - Log a mood event
  log --custom <name> <modifier> - Log custom event

  quests                  - List active quests
  quests history          - Show completed quests
  complete <id>           - Complete a quest
  create quest <title>    - Create a new quest

  traits                  - List active traits
  traits available        - List all available traits
  add trait <name>        - Add a trait
  remove trait <name>     - Remove a trait

  stats                   - Show overall statistics
  settings                - Show settings
  set <key> <value>       - Update a setting

  help                    - Show this help
  exit                    - Exit shell
```

## Test-Driven Development Plan

### Phase 1: Core Mood System (TDD)

**Test suite:** `tests/test_mood_system.py`

```python
# Test cases to write:
- test_calculate_mood_with_no_events()
- test_calculate_mood_with_positive_events()
- test_calculate_mood_with_negative_events()
- test_calculate_mood_with_traits()
- test_calculate_mood_with_expired_events()
- test_log_mood_event()
- test_mood_event_expiration()
- test_mood_faces_correct_for_scores()
- test_custom_mood_modifiers()
```

**Implementation:** `src/domain/mood.py`

### Phase 2: Quest System (TDD)

**Test suite:** `tests/test_quest_system.py`

```python
# Test cases to write:
- test_create_quest()
- test_get_active_quests()
- test_complete_quest_awards_xp()
- test_complete_quest_applies_mood_buff()
- test_complete_quest_with_additional_modifiers()
- test_quest_expiration()
- test_quest_categories()
- test_quest_history()
```

**Implementation:** `src/domain/quests.py`

### Phase 3: Trait System (TDD)

**Test suite:** `tests/test_trait_system.py`

```python
# Test cases to write:
- test_add_trait()
- test_remove_trait()
- test_trait_affects_mood()
- test_multiple_traits()
- test_trait_library()
```

**Implementation:** `src/domain/traits.py`

### Phase 4: Game Engine Integration (TDD)

**Test suite:** `tests/test_game_engine.py`

```python
# Test cases to write:
- test_engine_initialization()
- test_engine_state_persistence()
- test_engine_transaction_rollback()
- test_concurrent_operations()
```

**Implementation:** `src/engine.py`

### Phase 5: Shell Interface

**Test suite:** `tests/test_shell.py`

```python
# Test cases to write:
- test_shell_commands_execute()
- test_shell_output_formatting()
- test_shell_error_handling()
```

**Implementation:** `src/shell/`

### Phase 6: Rich TUI Refactor

**Refactor:** `src/ui/` to use engine API instead of direct DB access

## Implementation Order

1. **Set up testing infrastructure** (pytest, fixtures)
2. **Write mood system tests** (red)
3. **Implement mood system** (green)
4. **Write quest system tests** (red)
5. **Implement quest system** (green)
6. **Write trait system tests** (red)
7. **Implement trait system** (green)
8. **Build game engine wrapper** (integrates all systems)
9. **Build command shell** (uses engine API)
10. **Refactor Rich TUI** (uses engine API)

## Benefits of This Architecture

1. **Testability** - Business logic completely decoupled from UI
2. **Multiple frontends** - Shell, TUI, API all use same engine
3. **Debugging** - Shell makes it easy to inspect/modify state
4. **Scripting** - Can automate tasks via shell or Python scripts
5. **Future-proof** - Easy to add new frontends (web UI, mobile app, etc.)

## Open Questions

1. **Transaction handling** - Should engine support rollback for complex operations?
2. **Event system** - Should engine emit events that frontends can subscribe to?
3. **Caching strategy** - Where should caching live (engine or frontends)?
4. **Concurrency** - Do we need to worry about concurrent access (probably not for single-user)?

What do you think? Should we start with the test infrastructure and mood system?
