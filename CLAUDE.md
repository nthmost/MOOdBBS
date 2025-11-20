# MOOdBBS Project

## Project Overview

MOOdBBS is a local, always-on ASCII dashboard that combines mood tracking with a MUD/MOO-style quest system. It provides a RimWorld-inspired mood tracking system with buffs/debuffs, displays real-world quests for user exploration, and offers a nostalgic 90s BBS door game aesthetic.

**Key Goals:**
- Reflect mood buffs/debuffs in a non-judgmental, game-like way
- Suggest real-world quests and explorations
- Track moods using a RimWorld-inspired point system
- 100% ASCII-based with classic BBS feel
- Near-zero friction input via numpad

## Tech Stack (MVP)

- **UI Framework:** Rich (Python) for ASCII terminal interface
- **Database:** SQLite for persistence
- **Platform:** Linux/Pi with mini monitor (development on Mac)
- **Input:** Keyboard initially, transitioning to USB numpad
- **API:** Flask/FastAPI for local network integration

## Core Components

### 1. MOOdBBS Main Menu
- WanderMOO (quest system)
- MoodStats (view buffs/debuffs/traits)
- LogAction (manual mood logging)
- Settings (personalization)
- About

### 2. Mood Tracking System
- RimWorld-style mood modifiers (e.g., "Ate without table: -3")
- Aggregated mood score with ASCII face display
- Track: time indoors, social interaction, meal quality, quest completion, etc.
- User-selected RimWorld traits that affect mood calculations

### 3. Quest System (WanderMOO)
- Display up to 3 active quests
- Location-based suggestions (e.g., "Go to Coit Tower before 4pm")
- XP rewards on completion
- Track quest-related mood factors (got outdoors, visited new place, etc.)

### 4. Data Persistence
- Never destroy data; maintain full history
- Track activity and mood over time
- Weekly counters (reset Mondays)
- "N days ago" relative timestamps

### 5. API (Future)
- Log events from other devices
- Add quests programmatically
- Query current mood status
- LAN-based "security" for MVP

## File Structure

```
MOOdBBS/
├── CLAUDE.md              # This file - project instructions
├── MOOdBBS.md             # Project spec
├── MOOdBBS_mainmenu_mockup.md
├── MOOdBBS_cnxn_screen_mockup.md
├── MOOdBBS_Settings_mockup.md
├── MOOdBBS_About_mockup.md
├── MOOdStats_mockup.md
├── MOOdBBS_BuildRecs_from_ChatGPT.md
├── src/                   # Source code (to be created)
│   ├── ui/                # Rich-based UI components
│   ├── db/                # SQLite models and queries
│   ├── mood/              # Mood calculation logic
│   ├── quests/            # Quest generation and tracking
│   └── api/               # API endpoints (future)
├── data/                  # SQLite database location
├── tests/                 # Unit tests
└── README.md              # User-facing documentation
```

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use type hints for function signatures
- Document all public functions and classes
- Keep ASCII art and text content in separate config/data files

### Database Design
- Use SQLite with proper migrations
- Index commonly queried fields
- Store mood events with timestamps
- Maintain quest history and completion status
- Never delete user data (soft delete if needed)

### UI/UX Principles
- Maintain authentic 90s BBS aesthetic
- Keep all interactions numpad-friendly (numbers 0-9, Enter, Esc)
- Instant feedback for all user inputs
- Clear visual hierarchy with ASCII borders and spacing
- Use Rich library for colors, but keep it retro

### Testing
- Unit tests for mood calculations
- Integration tests for quest system
- Test database persistence across "reboots"
- Verify numpad input handling

## Task Status Reporting

When working on long-running or multi-step tasks in this project, create a task status file for monitoring:

### Status File Location
- **Location:** `~/.claude-monitor/moodbbs.json` (or multiple files for parallel tasks)
- **Purpose:** Allows external monitoring of Claude Code progress
- **Monitored by:** The `claude-monitor` tool at `~/projects/git/claude-monitor`
- **Note:** All projects deposit breadcrumbs in `~/.claude-monitor/` using project-specific filenames
- **Multiple Tasks:** Projects can create multiple JSON files (e.g., `moodbbs_ui.json`, `moodbbs_db.json`) to track parallel operations

### When to Create Status Files
- Multi-step tasks (3+ steps)
- Long-running operations (>30 seconds)
- Tasks that may need user intervention
- Background processes (database migrations, asset generation, testing)
- **Parallel tasks:** When using sub-agents or running tasks in parallel, create separate JSON files for each task

### Status File Format

```json
{
  "task_name": "Building MOOdBBS UI Components",
  "status": "in_progress",
  "progress_percent": 45,
  "current_step": "Creating main menu screen",
  "message": "Implementing Rich-based ASCII interface",
  "needs_attention": false,
  "updated_at": "2025-11-18T14:30:00Z"
}
```

### Status Values
- `pending` - Task queued but not started
- `in_progress` - Currently working on task
- `blocked` - Waiting for user input or external dependency
- `waiting` - Paused, will resume automatically
- `completed` - Task finished successfully
- `error` - Task failed, needs attention

### Required Fields
- `task_name` (string): Brief description of the task
- `status` (string): One of the status values above
- `updated_at` (string): ISO 8601 timestamp

### Optional Fields
- `progress_percent` (int): 0-100 completion percentage
- `current_step` (string): What's happening right now
- `message` (string): Additional context or status message
- `needs_attention` (bool): Set to `true` if user action required
- `tiny_title` (string): Short title for tiny display mode - when set, ONLY this is shown (not project/task/step) for maximum compactness (e.g., "Building UI", "Testing", "Migrating DB")

### For Claude Code: Use Write Tool

**IMPORTANT:** When creating/updating status files, Claude Code should use the **Write tool** directly, NOT Bash with heredocs.

```python
# Use the Write tool with file_path and JSON content
# Example:
Write(
    file_path="/Users/nthmost/.claude-monitor/moodbbs.json",
    content=json.dumps({
        "task_name": "Building MOOdBBS UI Components",
        "status": "in_progress",
        "progress_percent": 45,
        "current_step": "Creating main menu screen",
        "message": "Implementing Rich-based ASCII interface",
        "tiny_title": "Building UI",  # Optional: shows ONLY this in tiny mode
        "needs_attention": False,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }, indent=2)
)
```

This avoids permission prompts and is the correct tool for file operations.

### Update Frequency
- Update the file whenever status changes significantly
- For long operations, update every 5-10 seconds
- Always update when transitioning between states
- Always update when `needs_attention` becomes `true`

### Parallel Task Tracking

When Claude Code spawns multiple sub-agents or parallelizes work:

**Create separate status files for each parallel task:**
```python
# Main orchestration task
Write(
    file_path="~/.claude-monitor/moodbbs_main.json",
    content=json.dumps({
        "task_name": "Building MOOdBBS MVP",
        "status": "in_progress",
        "current_step": "Spawned 3 parallel build agents",
        "updated_at": datetime.now(timezone.utc).isoformat()
    }, indent=2)
)

# UI build (sub-agent 1)
Write(
    file_path="~/.claude-monitor/moodbbs_ui.json",
    content=json.dumps({
        "task_name": "Building UI components",
        "status": "in_progress",
        "progress_percent": 30,
        "current_step": "Creating main menu with Rich",
        "updated_at": datetime.now(timezone.utc).isoformat()
    }, indent=2)
)

# Database setup (sub-agent 2)
Write(
    file_path="~/.claude-monitor/moodbbs_db.json",
    content=json.dumps({
        "task_name": "Setting up database schema",
        "status": "in_progress",
        "progress_percent": 60,
        "current_step": "Creating mood_events table",
        "updated_at": datetime.now(timezone.utc).isoformat()
    }, indent=2)
)
```

**Benefits:**
- Each parallel task appears as a separate row in the monitor
- See progress of all parallel operations simultaneously
- Track which sub-agents need attention independently
- No file write conflicts between parallel tasks

### Cleanup
- Keep the status file until the task is truly finished
- Status files older than 24 hours are ignored by the monitor
- You can delete status files from `~/.claude-monitor/` after task completion if desired

## MVP Success Criteria

- [ ] Numpad inputs instantly reflect on ASCII dashboard
- [ ] Quest completion updates XP and reduces active quests list
- [ ] Quest completion flow prompts mood logging
- [ ] Mood score reacts appropriately to logged modifiers
- [ ] System survives reboot (data persists in SQLite)
- [ ] Clean 90s BBS aesthetic maintained throughout
- [ ] API allows: logging events, adding quests, querying mood status

## Future Features (Post-MVP)

- Ongoing text narrative / evolving personal lore
- Location-aware quests (GPS integration)
- Idle animations or "colony events"
- Mood-based environmental triggers (lights, soundscapes)
- Dedicated "Expedition Log" for places visited
- RimWorld-style memory system ("Had a fine meal," "Saw art," etc.)

## Notes for Claude Code

When working on this project:

1. **Aesthetic Consistency:** Maintain authentic 90s BBS feel across all components
2. **Numpad-First Design:** All interactions must work with numpad (0-9, Enter, Esc)
3. **Data Preservation:** Never destroy user data; soft delete or archive if needed
4. **Instant Feedback:** UI updates should be immediate and satisfying
5. **Task Tracking:** Use status files for multi-step operations (building UI, migrations, etc.)
6. **Mood Logic:** Follow RimWorld's mood system closely for MVP; can iterate later
7. **Quest Generation:** Keep quests realistic and location-appropriate for San Francisco
8. **Testing:** Verify persistence across restarts; this is critical for trust

## References

- RimWorld mood system: [RimWorld Wiki - Mood](https://rimworldwiki.com/wiki/Mood)
- Rich library docs: [https://rich.readthedocs.io/](https://rich.readthedocs.io/)
- SQLite Python docs: [https://docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html)
- Classic BBS aesthetics: [https://16colo.rs/](https://16colo.rs/)
