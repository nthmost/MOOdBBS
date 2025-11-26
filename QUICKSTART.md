# MOOdBBS Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running MOOdBBS

```bash
# TUI (Terminal User Interface) - Recommended
python tui.py

# Command Shell (for scripting)
python shell.py
```

## First Time Setup

On first run, MOOdBBS will:
1. Show the **Setup Wizard** (TUI only):
   - Enter your zipcode (validated for US/CA/UK formats)
   - Select transportation preferences (walking, biking, transit, car)
   - List museum/venue memberships (optional)

2. Create the SQLite database at `data/moodbbs.db`
3. Ready to start creating quests!

Your profile settings are saved and can be updated anytime in Settings.

## Basic Usage

### Boot Screen
- Press ENTER to continue past the ASCII art

### Dashboard
Shows:
- Current mood score and face (`:D`, `:)`, `:|`, `:(`, `D:`)
- Up to 3 active quests
- Recent mood events

### Main Menu
1. **WanderMOO** - Quest system
   - Create quests (smart mode with LLM or manual)
   - View active quests
   - Complete quests
   - Manage quests (delete individual or destroy all)

2. **MoodStats** - Mood details
   - View current mood score
   - See active traits
   - See active mood modifiers

3. **LogAction** - Manual mood logging
   - Quick log common events
   - Create custom events
   - Events affect mood immediately

4. **Settings** - Profile configuration
   - Update zipcode
   - Change transportation preferences
   - Manage memberships

5. **About** - Project info

## Keyboard Controls

- **1-5**: Menu selection
- **m**: Show main menu from dashboard
- **q**: Quit application
- **ENTER**: Continue/return to previous screen

## Sample Mood Events

Pre-configured events in LogAction:
- Ate without table: -3
- Had a fine meal: +5
- Social interaction: +8
- Completed a walk: +6
- Too long indoors: -5
- Saw something beautiful: +4

## Understanding Mood Scores

- **20+**: Very Happy `:D`
- **10-19**: Happy `:)`
- **0-9**: Neutral `:|`
- **-1 to -9**: Unhappy `:(`
- **-10 or lower**: Very Unhappy `D:`

Mood is calculated from:
- Active mood events (with 24h default duration)
- User traits (permanent modifiers)

## Sample Quests

Default quests for San Francisco:
1. Visit Coit Tower before sunset (15 XP)
2. Get coffee at a new cafe (10 XP)
3. Walk to the ocean (20 XP)

## Data Persistence

All data persists in `data/moodbbs.db`:
- Mood events
- Quests and completions
- Traits
- Mood snapshots

Safe to restart anytime - your data is preserved!

## Tips

1. Log events as they happen for accurate mood tracking
2. Complete quests to clear them from your dashboard
3. Check MoodStats to understand why your mood is where it is
4. The app saves a mood snapshot on exit for history tracking

## Troubleshooting

**Rich library not found:**
```bash
pip install rich
```

**Database errors:**
Delete `data/moodbbs.db` to start fresh (you'll lose your data)

**Screen too small:**
MOOdBBS is designed for terminal windows at least 80 columns wide

## Next Steps

- Add your own quests via the database
- Customize mood events in `src/main.py`
- Add your own RimWorld traits
- Build the API for home automation integration

Enjoy tracking your mood the RimWorld way! 🎮
