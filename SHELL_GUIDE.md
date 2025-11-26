# MOOdBBS Shell Guide

## Quick Start

```bash
# Launch the shell
python shell.py

# Or with virtual environment
source venv/bin/activate && python shell.py
```

## Available Commands

### Mood System

**View current mood:**
```
moodbbs> mood
```

**Show available mood modifiers:**
```
moodbbs> log
```

**Log a mood event:**
```
moodbbs> log fine_meal
moodbbs> log social_interaction
moodbbs> log ate_without_table
```

**Log custom event:**
```
moodbbs> log custom "BART delayed again" -5
moodbbs> log custom "Perfect weather" 3
```

### Quest System

**List active quests:**
```
moodbbs> quests
```

**Show completed quests:**
```
moodbbs> quests history
```

**Create a new quest:**
```
moodbbs> create quest
```
(Interactive prompts for title, description, category, difficulty)

**Complete a quest:**
```
moodbbs> complete 1
```
(Prompts for additional mood modifiers)

**Snooze a quest:**
```
moodbbs> snooze 2
```
(Prompts for reason: weather, time, mood, or custom)

**Hide a quest permanently:**
```
moodbbs> hide 3
```

### Traits

**Show active traits:**
```
moodbbs> traits
```

**Add a trait:**
```
moodbbs> traits add Optimist
```
(Prompts for description and mood modifier)

### Statistics

**Show overall stats:**
```
moodbbs> stats
```

## Example Session

```
$ python shell.py

MOOdBBS Shell v0.1.0
Type 'help' for commands, 'exit' to quit

moodbbs> create quest
Title: Walk to Green Apple Books
Description: Browse the new releases
Category:
  1. Social
  2. Constitutional
  3. Creative
  4. Experiential
Select: 2

Difficulty:
  1. Easy (5-10 XP)
  2. Medium (15-20 XP)
  3. Hard (25-35 XP)
  4. Extreme (40-50 XP)
Select: 1

Quest created! Added to active quests.
1. Walk to Green Apple Books [10 XP]

moodbbs> log fine_meal
Logged: Had a fine meal (+5)
Mood updated: :) +5

moodbbs> mood

Current Mood: :) +5

Active Modifiers:
  +5 fine_meal
      Had a fine meal

moodbbs> complete 1

Quest completed! +10 XP
Total XP: 10

Mood buffs applied:
  +5 quest_completed
  +6 constitutional_activity

Log additional modifiers? (y/n): y

Quick options:
  1. Pain (-)
  2. Energized (+)
  3. Beautiful view (+4)
  4. Social interaction (+8)
  5. Custom...
  d. Done

Select: 3
Added: Beautiful view (+4)

Select: d

Mood updated: :D +20

moodbbs> stats

MOOdBBS Statistics

Total XP:          10
Quests Completed:  1
Current Mood:      +20
Active Traits:     0
Active Modifiers:  4

moodbbs> exit

Goodbye!
```

## Tips

- Use `help` to see all available commands
- Tab completion not yet implemented (coming soon)
- Commands are case-insensitive
- Ctrl+C to cancel current input
- Ctrl+D or `exit` to quit

## Architecture

The shell demonstrates the **headless game engine** architecture:

```
Shell (REPL)
    ↓
Game Engine
    ↓
Domain Layer (Mood + Quest systems)
```

All game logic is in the domain layer, making it easy to:
- Add new interfaces (TUI, web UI, API)
- Test business logic independently
- Swap out data persistence layers
- Script automation tasks

## Next Steps

- Try creating different types of quests
- Experiment with custom mood modifiers
- Track your mood patterns over a week
- Add traits that match your personality
