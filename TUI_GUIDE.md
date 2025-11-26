# MOOdBBS TUI Guide

## Quick Start

```bash
# Launch the TUI
python tui.py

# Or with virtual environment
source venv/bin/activate && python tui.py
```

## Overview

The MOOdBBS TUI provides a nostalgic 90s BBS-style interface with Rich terminal graphics. It features:

- ASCII art boot screen with connection animation
- **First-run setup wizard** for personalized experience
- Box-drawing character menus
- Color-coded mood indicators
- Interactive quest management with **LLM-powered smart creation**
- Real-time mood tracking
- **Settings menu** for updating profile

## Navigation

The TUI uses numbered menu options for navigation:

### Main Menu

1. **WanderMOO** - Quest management system
2. **MoodStats** - View current mood, traits, and modifiers
3. **LogAction** - Log mood-affecting events
4. **Settings** - Configuration (coming soon)
5. **About** - System information
q. **Quit** - Exit MOOdBBS

## Screens

### Boot Screen

The boot screen displays:
- ASCII cow art (classic MOO reference)
- "Connecting to MOOdBBS..." animation
- CONNECT 2400 (nostalgic BBS modem speed)
- Welcome message

### First-Run Setup Wizard

On first launch, you'll see a quick 3-step setup wizard:

**Step 1: Location**
- Enter your zipcode (validated for US, CA, UK formats)
- Supports: 94118 or 94118-1234 (US), A1A 1A1 (CA), SW1A 1AA (UK)
- Helps suggest location-relevant quests
- Can skip if desired

**Step 2: Transportation**
- Select how you get around: walking, biking, transit, car
- Multi-select (choose all that apply)
- Quick "all of the above" option
- Affects quest suggestions

**Step 3: Memberships**
- List museum/venue memberships (comma-separated)
- Examples: Cal Academy, SFMOMA, de Young, Exploratorium
- Used for low-friction quest suggestions
- Adjusts quest XP (membership = easier access = lower XP)

After setup, your profile is saved and you won't see the wizard again.

### MoodStats Screen

Shows your current psychological state:

```
Current Mood: :D +20

Active Traits:
  +3 Optimist
      Generally looks on bright side

Active Modifiers:
  +5 fine_meal
      Had a fine meal
  +6 constitutional_activity
      Went for a good walk
```

Features:
- Mood face indicator (:D, :), :|, :(, D:)
- Numeric mood score
- Active traits with descriptions
- Current mood modifiers with timestamps

### WanderMOO (Quest System)

Quest management interface with options:

**[c] Create new quest** - Two creation modes:

*Smart Mode (LLM-powered):*
- Just type what you want to do in natural language
- Examples: "Visit Cal Academy on a weekday", "First Friday poetry at Coit Tower"
- LLM extracts: title, category, XP, renewal frequency, time constraints
- **Edit mode** - Review and edit XP, category, or title before creating
- Choose renewal frequency (one-time, daily, weekly, monthly, seasonal)
- Accounts for your memberships (reduces XP for easy access)

*Manual Mode:*
- Enter title and description
- Select category (Social, Constitutional, Creative, Experiential)
- Choose difficulty (Easy/Medium/Hard/Extreme)
- Set renewal policy
- Automatic XP reward calculation

**[x] Complete quest** - Mark quest as done:
- Enter quest ID
- Automatic mood buff application
- XP reward granted
- Category-specific bonuses added

**[s] Snooze quest** - Temporarily hide quest:
- Optional feedback (Weather, Time, Mood, Custom)
- Quest remains active but hidden

**[h] View history** - See completed quests:
- Full list of finished quests
- XP earned per quest

**[m] Manage quests** - Quest management submenu:
- **Delete a quest** - Remove individual quest permanently
- **Destroy ALL quest data** - Reset all quests (requires typing "DESTROY")
  - Removes all quests, completions, and XP
  - Preserves your profile settings

**[b] Back to menu**

Active quests display:
```
Active Quests:
  [1] Walk to Green Apple Books [10 XP]
      Browse the new releases
      Constitutional | daily
```

### LogAction Screen

Quick mood event logging:

Quick options show common mood modifiers:
```
1. +5 Had a fine meal
2. +8 Social interaction
3. -3 Ate without table
4. +4 Beautiful view
...
9. Custom event
0. Cancel
```

For custom events:
- Enter description
- Specify modifier (+/- value)
- Immediately applied to mood

### About Screen

Displays:
- MOOdBBS version
- System description
- Credits
- Architecture info

### Settings Screen

Update your profile anytime:

**Current Profile Display:**
- Shows current zipcode, transportation preferences, memberships
- Easy reference to see what's configured

**[z] Change zipcode:**
- Update your postal code
- Same validation as setup wizard
- Shows current value before changing

**[t] Update transportation preferences:**
- Multi-select: walking, biking, transit, car
- Quick "all of the above" option
- Updates saved immediately

**[m] Manage memberships:**
- Add/update museum and venue memberships
- Shows current list
- Can clear all with confirmation
- Affects quest XP calculations

**[b] Back to menu**

All changes are saved immediately to your profile.

## Color Coding

The TUI uses consistent color coding:

- **Cyan** - Headers, titles, section labels
- **Yellow** - Prompts, quest IDs, choices
- **Green** - Positive modifiers, success messages
- **Red** - Negative modifiers, errors
- **Dim/Gray** - Descriptions, metadata

## Tips

- All screens can be exited by following on-screen prompts
- Quest IDs are shown in brackets [1], [2], etc.
- Mood modifiers show +/- signs for clarity
- Color coding helps distinguish positive vs negative effects
- The boot animation only shows on first launch
- **Smart quest creation** uses Ollama LLM - requires running instance
- Press Enter to skip/cancel most inputs
- Validation loops let you retry on errors (like invalid zipcodes)

## Architecture

The TUI demonstrates the **headless game engine** architecture:

```
TUI (Rich-based interface)
    ↓
Game Engine
    ↓
Domain Layer (Mood + Quest systems)
```

All game logic is in the domain layer. The TUI is just one possible frontend. You can:
- Use the command shell (shell.py) for scripting
- Build a web interface (future)
- Create an API (future)
- Run headless for automation

## Example Session

```
$ python tui.py

[Boot screen with cow ASCII art]
[Connection animation]

MOOdBBS Main Menu

1. WanderMOO
2. MoodStats
3. LogAction
4. Settings
5. About
q. Quit

Select option: 1

[WanderMOO screen]
No active quests. Create one to get started!

Options:
  [c] Create new quest
  [x] Complete quest
  [s] Snooze quest
  [h] View history
  [b] Back to menu

Select: c

Title: Walk to Green Apple Books
Description: Browse new releases in Clement St
Category:
  1. Social
  2. Constitutional
  3. Creative
  4. Experiential
Select (1-4): 2

Difficulty:
  1. Easy (5-10 XP)
  2. Medium (15-20 XP)
  3. Hard (25-35 XP)
  4. Extreme (40-50 XP)
Select (1-4): 1

Quest created! [1] Walk to Green Apple Books

[Returns to WanderMOO]

Active Quests:
  [1] Walk to Green Apple Books [10 XP]
      Browse new releases in Clement St
      Constitutional | daily

Select: x

Quest ID to complete: 1

Quest completed! +10 XP

Mood buffs applied:
  +5 quest_completed
  +6 constitutional_activity

[Back to main menu]
```

## Keyboard Shortcuts

Currently all navigation is via numbered menu options. Future enhancements:

- Arrow key navigation
- Numpad support (for kitchen display mode)
- Vim-style hjkl navigation
- Tab completion

## Next Steps

- Try creating different types of quests
- Log various mood events to see mood changes
- Complete quests to earn XP and mood buffs
- Watch your mood score evolve throughout the day
- Check MoodStats to understand what's affecting you

## Troubleshooting

**TUI not displaying colors?**
- Ensure your terminal supports ANSI colors
- Try a modern terminal (iTerm2, Windows Terminal, etc.)

**Box-drawing characters look broken?**
- Your terminal may not support Unicode box-drawing
- Use a terminal with full Unicode support

**TUI crashes on input?**
- Ensure you're running interactively (not in background)
- Check Python version (3.8+ required)
