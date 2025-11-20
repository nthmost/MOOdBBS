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
python src/main.py
```

## Usage

### Main Menu Options

1. **WanderMOO** - View and complete quests
2. **MoodStats** - View current mood score, traits, and active modifiers
3. **LogAction** - Manually log mood-affecting events
4. **Settings** - Personalization (coming soon)
5. **About** - Project info

### Sample Mood Events

- Ate without table: -3
- Had a fine meal: +5
- Social interaction: +8
- Completed a walk: +6
- Too long indoors: -5
- Saw something beautiful: +4

### Controls

- **1-5**: Select menu options
- **m**: Show main menu
- **q**: Quit application
- **ENTER**: Continue/return

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
- [x] Quest completion can trigger mood logging
- [x] Mood score reacts to logged modifiers
- [x] System survives reboot (SQLite persistence)
- [x] Clean 90s BBS aesthetic
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
