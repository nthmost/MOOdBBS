# MOOdBBS Changelog

## [Unreleased]

### Added - Moodlet System Overhaul (2025-11-26)

#### Core Features
- **QuickLog Interface**: Replaced LogAction with categorized moodlet browser
  - Browse 33+ moodlets by category (Creative, Food, Self-Care, Social)
  - One-press application
  - Custom moodlet creation (LLM suggestions pending)

- **New Moodlet Categories**:
  - **Self-Care** (6 moodlets): Haircuts, nails, baths, showers, skincare, comfort TV
  - **System** (1 moodlet): First login welcome bonus

#### Moodlet Library Expansion

**Food Category** (9 total):
- Added "Ate a fine meal" (+6, 4h)
- Added "Ate a lavish meal" (+9, 6h)
- Added alcohol moodlets with negative backoff (hangover mechanic):
  - "Had a drink" (+4, 2h → -2, 12h)
  - "Had a few drinks" (+6, 3h → -3, 12h)
  - "Got tipsy" (+8, 4h → -4, 12h)
  - "Whiskey warmth" (+4, 1h → -2, 12h)

**Social Category** (13 total):
- Added "Gave someone a compliment" (+2, 2h)
- Added flirting moodlets:
  - "Flirted (welcome)" (+5, 4h)
  - "Flirted (unwelcome)" (-5, 2h)
- Added negative social moodlets:
  - "Rejected" (-10, 24h → -5, 12h)
  - "Dumped (casual)" (-8, 48h → -4, 48h)
  - "Dumped (serious)" (-15, 72h → -8, 120h)
  - "Dumped (long-term)" (-25, 168h → -12, 336h)
  - "Friend breakup" (-12, 96h → -6, 72h)

**Self-Care Category** (6 new):
- "Took a hot shower" (+3, 2h)
- "Took a bath" (+5, 3h)
- "Got my nails done" (+5, 4h → +3, 120h)
- "Did my skin care routine" (+5, 12h)
- "Got a great haircut" (+10, 8h → +4, 120h)
- "Watching comfort TV/movie" (+10, 1h)

**System Category** (1 new):
- "Joined MOOdBBS!" (+5, 24h) - Applied automatically on first login

#### UI/UX Improvements
- Fixed moodlet display: removed "custom" labels, hid underscores in event types
- Adjusted mood face thresholds for better symmetry:
  - `:D` = 16+ (was 20+)
  - `:)` = 6-15 (was 10-19)
  - `:|` = -5 to 5 (was 0-9)
  - `:(` = -15 to -6 (was -9 to -1)
  - `D:` = -16 or lower (was -10 or lower)
- Bordered mood display panel in MoodStats
- Clean display of active moodlets with descriptions

#### Database
- 7 new migrations (001-007)
- Database schema supports negative backoff values for hangovers
- Proper moodlet expiration and backoff phase transitions
- 33+ total event-based moodlets across 8 categories

#### Admin Tool
- **New**: `admin.py` - Shell-based administrative interface
  - Database status and statistics
  - Safe database reset with automatic backup
  - Manual backup creation
  - View user profile
  - Clear active moodlets/quests
  - Moodlet and quest statistics
  - Migration runner

#### Documentation
- Updated MOODLET_SYSTEM_SPEC.md with complete moodlet inventory
- Updated QUICKSTART.md with QuickLog usage and new mood thresholds
- Updated README.md with moodlet system overview and admin tool section
- Added ADMIN_GUIDE.md with comprehensive admin tool documentation
- Added .clauderc for tool permissions

#### Testing
- Created test_quicklog.py with 3 automated tests
- All tests passing (category loading, positive/negative moodlet application)
- Verified moodlet stacking and expiration mechanics

### Changed
- Renamed "LogAction" to "QuickLog" throughout codebase
- Mood calculation now uses moodlet-specific durations instead of 24h default
- MoodStats displays moodlet descriptions intelligently

### Technical
- MOOdBBSEngine methods: `apply_moodlet()`, `get_active_moodlets()`, `cleanup_expired_moodlets()`
- Database methods: `get_moodlets_by_category()`, `get_all_event_moodlets()`
- Backoff phase tracking with `is_in_backoff` flag
- Proper ISO timestamp handling for moodlet expiration

## Future Enhancements

### Pending Implementation
- [ ] Quest completion feedback (difficulty rating + location favoriting)
- [ ] LLM-suggested custom moodlets in QuickLog
- [ ] LLM-generated starter quests on first login
- [ ] Quest completion triggers category-specific moodlet menu
- [ ] Negative moodlet expansion (drugs, ADHD meds, etc.)
- [ ] Weather-dependent moodlets
- [ ] Combo/streak bonuses

### Known Issues
- None currently

---

## Version History

### v0.2.0 - Moodlet System (2025-11-26)
Complete overhaul of mood tracking with RimWorld-inspired moodlet system

### v0.1.0 - MVP (2025-11-18)
Initial release with basic quest system and mood tracking
