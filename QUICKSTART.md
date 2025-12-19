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

3. **QuickLog** - Manual mood logging (moodlets)
   - Browse moodlets by category (Creative, Food, Self-Care, Social)
   - One-press application
   - Create custom moodlets
   - Moodlets affect mood immediately with durations

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

## Sample Moodlets

Pre-configured moodlets available in QuickLog by category:

**Food:**
- Ate a fine meal: +6 (4h)
- Ate a lavish meal: +9 (6h)
- Had a drink: +4 (2h → -2, 12h hangover)
- Ate without table: -3 (2h)

**Social:**
- Gave someone a compliment: +2 (2h)
- Hugged: +5 (3h)
- Flirted (welcome): +5 (4h)
- Rejected: -10 (24h → -5, 12h)
- Dumped (serious): -15 (72h → -8, 120h)

**Self-Care:**
- Took a hot shower: +3 (2h)
- Got a great haircut: +10 (8h → +4, 120h)
- Watching comfort TV: +10 (1h)

**Creative:**
- Problem Solved: +6 (6h)
- Work Praised: +8 (8h)
- Project Finished: +10 (12h)

## Understanding Mood Scores

- **16+**: Very Happy `:D`
- **6-15**: Happy `:)`
- **-5 to 5**: Neutral `:|`
- **-15 to -6**: Unhappy `:(`
- **-16 or lower**: Very Unhappy `D:`

Mood is calculated from:
- Active moodlets (with specific durations, some with backoff phases)
- User traits (permanent modifiers)
- First-time login bonus: +5 for 24h

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
