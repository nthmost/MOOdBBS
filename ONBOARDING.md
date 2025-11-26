# MOOdBBS Onboarding Guide for Claude Code

**Purpose**: Get up to speed on project status in <5 minutes without wasted tool calls.

## Quick Orientation (Run These First)

```bash
# 1. Check what's running
ls -la data/moodbbs.db  # Database exists?

# 2. Get codebase stats
find src -name "*.py" | wc -l  # How many Python files
find src -name "*.py" | xargs wc -l | tail -1  # Total LOC

# 3. Check database state
sqlite3 data/moodbbs.db ".tables"  # What tables exist
sqlite3 data/moodbbs.db "SELECT COUNT(*) FROM quests WHERE status = 'active';"
sqlite3 data/moodbbs.db "SELECT * FROM user_profile LIMIT 1;"

# 4. Run tests
source venv/bin/activate && python -m pytest tests/ -v --tb=short

# 5. Check what's implemented
ls -la src/  # Top-level modules
ls -la src/tui/  # TUI components
ls -la src/services/  # External services
ls -la src/domain/  # Domain models
```

## Project Structure (DON'T Read These as Files - They're Directories!)

```
MOOdBBS/
├── CLAUDE.md              # Project instructions (READ THIS FIRST)
├── QUICKSTART.md          # User guide (READ THIS SECOND)
├── product/               # 📁 DIRECTORY - Product specs
│   ├── QUEST_SYSTEM_SPEC.md
│   ├── PRODUCT_VISION.md
│   ├── TECHNICAL_REQUIREMENTS.md
│   └── USER_PERSONAS.md
├── src/                   # 📁 DIRECTORY - Source code
│   ├── engine.py          # Core game engine (READ THIS)
│   ├── main.py            # Legacy main (may have duplication)
│   ├── domain/            # 📁 Domain models
│   │   ├── mood.py        # Mood calculation system
│   │   ├── quests.py      # Quest domain logic
│   │   ├── traits.py      # RimWorld-style traits
│   │   └── user_profile.py
│   ├── database/          # 📁 Database layer
│   │   └── db.py          # SQLite operations
│   ├── tui/               # 📁 Terminal UI
│   │   ├── app.py         # TUI application
│   │   └── screens.py     # Rich-based screens
│   ├── services/          # 📁 External services
│   │   ├── llm_quest_parser.py
│   │   └── zipcode_validator.py
│   └── shell/             # 📁 Shell interface
├── tests/                 # 📁 Unit tests (44 tests, all passing)
├── config/                # 📁 Configuration files
├── data/                  # 📁 SQLite database location
│   └── moodbbs.db         # The actual database
├── shell.py               # Shell entry point
├── tui.py                 # TUI entry point
└── venv/                  # 📁 Python virtual environment
```

## Key Files to Read for Context

**Read in this order:**

1. `CLAUDE.md` - Project instructions, conventions, status file format
2. `QUICKSTART.md` - What works right now, user-facing features
3. `src/engine.py` (first 100 lines) - Core API and architecture
4. `src/domain/quests.py` (first 100 lines) - Quest data model
5. `product/QUEST_SYSTEM_SPEC.md` (first 100 lines) - Quest design philosophy

**Don't read unless specifically needed:**
- Anything in `venv/` (virtual environment packages)
- Anything in `__pycache__/` (Python bytecode)
- `product/mockups/` (old mockup files)

## Common Tasks - Fast Paths

### Task: "What's the project status?"

```bash
# Database stats
sqlite3 data/moodbbs.db <<EOF
SELECT COUNT(*) as total_quests FROM quests;
SELECT COUNT(*) as active_quests FROM quests WHERE status = 'active';
SELECT COUNT(*) as completed_quests FROM quest_completions;
SELECT COUNT(*) as mood_events FROM mood_events;
SELECT * FROM user_profile;
EOF

# Code stats
find src -name "*.py" -not -path "*/venv/*" | xargs wc -l | tail -1

# Test status
source venv/bin/activate && python -m pytest tests/ -q
```

### Task: "How does the quest system work?"

```bash
# Read these in order
cat src/domain/quests.py | head -150  # Data models
cat src/engine.py | grep -A 20 "def.*quest"  # Quest methods
cat product/QUEST_SYSTEM_SPEC.md | head -200  # Design spec
```

### Task: "How does mood tracking work?"

```bash
cat src/domain/mood.py | head -150
cat src/engine.py | grep -A 20 "def.*mood"
```

### Task: "What's in the database?"

```bash
sqlite3 data/moodbbs.db <<EOF
.schema quests
.schema mood_events
.schema user_profile
SELECT * FROM quests LIMIT 5;
SELECT * FROM mood_events ORDER BY created_at DESC LIMIT 10;
EOF
```

## What's Implemented (As of Nov 2025)

### ✅ Complete
- Mood calculation system (RimWorld-style)
- Quest lifecycle (create, complete, snooze, hide, renew)
- TUI with Rich library (boot screen, dashboard, main menu)
- SQLite persistence (8 tables)
- User profile & setup wizard
- Test suite (44 tests, 100% pass rate)
- LLM quest parser service
- Zipcode validation

### 🚧 Partial
- Quest auto-renewal (designed but may need refinement)
- Mood modifier library (basic set exists, needs expansion)
- API (directory exists but empty)

### ❌ Not Started
- Quest template library (0 active quests in DB)
- API implementation (Flask/FastAPI)
- Mood history visualization
- Numpad hardware integration
- Location-aware quest generation
- Idle animations
- Memory system

## Anti-Patterns to Avoid

### ❌ Don't Do This
```bash
# Reading directories as files
Read("/Users/nthmost/projects/git/MOOdBBS/src/services")
Read("/Users/nthmost/projects/git/MOOdBBS/product")

# Using grep/find when database queries are better
grep "quest" src/**/*.py  # Too broad
find . -name "*.py" -exec grep "quest" {} \;  # Slow

# Running pytest without activating venv
pytest tests/  # Will fail

# Forgetting to check if database exists
sqlite3 nonexistent.db "SELECT * FROM quests"  # Error
```

### ✅ Do This Instead
```bash
# List directory contents first
ls -la src/services/
ls -la product/

# Use database for data questions
sqlite3 data/moodbbs.db "SELECT title FROM quests WHERE status = 'active';"

# Activate venv for Python commands
source venv/bin/activate && python -m pytest tests/

# Check file existence
[ -f data/moodbbs.db ] && echo "DB exists" || echo "DB missing"
```

## Status File Updates

**IMPORTANT**: Update `/Users/nthmost/.claude-monitor/moodbbs.json` during long tasks.

### When to Update
- Multi-step tasks (3+ steps)
- Long operations (>30 seconds)
- When spawning sub-agents
- Before asking user questions
- When blocked/errored

### Quick Update Pattern
```bash
cat > /Users/nthmost/.claude-monitor/moodbbs.json << 'EOF'
{
  "task_name": "Brief task description",
  "status": "in_progress",
  "progress_percent": 50,
  "current_step": "What I'm doing right now",
  "message": "Additional context",
  "tiny_title": "Short",
  "needs_attention": false,
  "updated_at": "2025-11-25T23:30:00Z"
}
EOF
```

## Test-Driven Development

### Before making changes
```bash
# Run existing tests
source venv/bin/activate && python -m pytest tests/ -v

# Check specific test file
python -m pytest tests/test_quest_system.py -v
python -m pytest tests/test_mood_system.py -v
```

### After making changes
```bash
# Run full suite
python -m pytest tests/ -v --tb=short

# Run with coverage (if available)
python -m pytest tests/ --cov=src --cov-report=term-missing
```

## Quick Reference: File Purposes

| File | Purpose | When to Read |
|------|---------|-------------|
| `CLAUDE.md` | Project instructions | Always (first file) |
| `QUICKSTART.md` | User guide | Understanding features |
| `src/engine.py` | Core game API | Understanding architecture |
| `src/domain/quests.py` | Quest models | Quest-related work |
| `src/domain/mood.py` | Mood models | Mood-related work |
| `src/database/db.py` | Database layer | Database operations |
| `src/tui/screens.py` | TUI screens | UI changes |
| `product/QUEST_SYSTEM_SPEC.md` | Quest design | Quest feature design |
| `tests/test_*.py` | Unit tests | Understanding behavior |

## Emergency Checks

If something seems wrong:

```bash
# 1. Is the database corrupted?
sqlite3 data/moodbbs.db "PRAGMA integrity_check;"

# 2. Are tests passing?
source venv/bin/activate && python -m pytest tests/ -x  # Stop on first failure

# 3. Can the app start?
source venv/bin/activate && python shell.py --help

# 4. Is venv set up correctly?
source venv/bin/activate && python --version
pip list | grep -E "(rich|pytest)"

# 5. What's the git status?
git status --short
git log --oneline -5
```

## Questions to Ask User

If context is unclear after reading files:

1. "What's the priority: quest generation, API, mood expansion, or something else?"
2. "Are there any blocking bugs I should know about?"
3. "What's working well that I should preserve?"
4. "What's the target deployment environment?" (Pi, Mac, Linux server)
5. "Any user feedback to consider?"

## Time-Saving Patterns

### Pattern: Get Project Status
1. Read `QUICKSTART.md` (30 seconds)
2. Check database stats (10 seconds)
3. Run tests (20 seconds)
4. Summarize findings to user (30 seconds)
**Total: ~90 seconds**

### Pattern: Implement New Feature
1. Read relevant domain model (30 seconds)
2. Check existing tests (20 seconds)
3. Read engine.py for similar patterns (30 seconds)
4. Implement + test (varies)
5. Update QUICKSTART.md if user-facing (20 seconds)
**Total: ~100 seconds + implementation time**

### Pattern: Debug Issue
1. Reproduce in tests (30 seconds)
2. Check database state (10 seconds)
3. Read relevant source (30 seconds)
4. Fix + verify (varies)
**Total: ~70 seconds + fix time**

## Remember

- **The database is the source of truth** - Check it first for data questions
- **Tests are documentation** - Read them to understand behavior
- **Product specs are aspirational** - Check engine.py for what's actually implemented
- **Update status file for long tasks** - User is monitoring progress
- **Directories are not files** - Use `ls` first, then read specific files
- **Activate venv for Python** - Always `source venv/bin/activate` first
