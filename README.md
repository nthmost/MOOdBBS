# MOOdBBS

A local, always-on ASCII dashboard that combines RimWorld-style mood tracking with a MUD/MOO-style quest system. Built with authentic 90s BBS aesthetics.

## Features

- **Mood Tracking**: RimWorld-inspired mood system with buffs/debuffs
- **Quest System**: Location-aware daily quests for San Francisco
- **ASCII Interface**: Classic 90s BBS door game feel with Rich library
- **Persistent Data**: SQLite database survives restarts
- **Numpad Navigation**: Simple 1-5 number-based menu system

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run MOOdBBS:
```bash
# TUI (Terminal User Interface) - Recommended
python tui.py

# Admin Tool
python admin.py

# Command Shell (for scripting)
python shell.py
```

## Usage

### Main Menu Options

1. **WanderMOO** - View and complete quests
2. **MoodStats** - View current mood score, traits, and active moodlets
3. **QuickLog** - Browse and apply moodlets by category
4. **Settings** - Profile configuration (zipcode, transport, memberships)
5. **About** - Project info

### Moodlet System

MOOdBBS uses a RimWorld-inspired moodlet system with:
- **8 categories**: Creative, Culture, Exercise, Exploration, Food, Rest, Self-Care, Social
- **33+ pre-configured moodlets** with varying durations (1-168 hours)
- **Backoff mechanics**: Some moodlets have two phases (e.g., haircut stays nice for days)
- **Negative backoffs**: Alcohol provides temporary boost with hangover effect later
- **Relationship tracking**: Breakups/rejections scale by severity with extended recovery periods

### Controls

- **1-5**: Select menu options
- **m**: Show main menu
- **q**: Quit application
- **ENTER**: Continue/return

### Admin Tool

The admin tool (`admin.py`) provides database management and statistics:

**Database Operations:**
- View database status and table statistics
- Reset database safely (with backup)
- Create manual backups
- Run migrations

**Data Management:**
- View user profile
- Clear active moodlets
- Clear active quests

**Statistics:**
- Moodlet statistics by category
- Most applied moodlets
- Quest completion statistics
- XP tracking

Run with: `python admin.py`

## Project Structure

```
MOOdBBS/
├── src/
│   ├── main.py          # Main application entry point
│   ├── db/
│   │   └── models.py    # Database models and operations
│   └── ui/
│       └── main_menu.py # Rich-based UI components
├── data/                # SQLite database location
├── tests/               # Unit tests (coming soon)
└── requirements.txt     # Python dependencies
```

## MVP Success Criteria

- [x] Numpad inputs work and reflect on dashboard
- [x] Quest completion updates and reduces active quest list
- [x] Moodlet system with 33+ pre-configured moodlets
- [x] QuickLog categorized browser interface
- [x] Backoff mechanics (positive and negative)
- [x] Mood score reacts to active moodlets
- [x] System survives reboot (SQLite persistence)
- [x] Clean 90s BBS aesthetic
- [x] First login welcome bonus
- [ ] Quest completion triggers moodlet selection (coming soon)
- [ ] LLM-suggested custom moodlets (coming soon)
- [ ] API for external integration (coming soon)

## Future Features

- Location-aware quests using GPS
- Idle animations and "colony events"
- Mood-based environmental triggers
- Expedition log for places visited
- RimWorld-style memory system
- API for home automation integration

## License

Free to use and modify for personal projects.

## Credits

i made this with my own hooves 🐴
