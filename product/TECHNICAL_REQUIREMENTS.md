# MOOdBBS Technical Requirements

## Display Requirements

### Multi-Size Support
Following the claude-monitor model, MOOdBBS must support multiple display sizes:

#### Tiny Mode (Default)
- **Target:** Very small displays (e.g., 480x320 or similar)
- **Layout:** Ultra-minimal, essential info only
- **Columns:** Status emoji, Task/Info (flexible), Progress bar (small), Updated time
- **Use case:** Kitchen wall-mounted mini display

#### Small Mode
- **Target:** Small displays (e.g., 800x600)
- **Layout:** Compact with progress indicators
- **Use case:** Raspberry Pi with 7" display

#### Medium Mode
- **Target:** Standard monitors (e.g., 1024x768)
- **Layout:** Clean columnar, no progress bars
- **Use case:** Dedicated desktop monitor

#### Large Mode
- **Target:** Wide/high-res displays (1920x1080+)
- **Layout:** Maximum information density
- **All fields visible:** Status, details, messages, percentages
- **Use case:** Main desktop display in dual-monitor setup

### Display Configuration
- Size mode configurable via Settings or command-line arg
- Automatically adjust on terminal resize (future enhancement)
- Save preferred size mode in database settings

## Input Requirements

### Phase 1: Full Keyboard
**Current implementation** - Learning phase
- Standard QWERTY keyboard
- Number keys 1-9 for menu navigation
- Enter/Return for confirmation
- ESC for cancel/back (future)
- Arrow keys for list navigation (future)

### Phase 2: Numpad Primary
**Target implementation** - Production use
- **0-9** for menu selection and numeric input
- **Enter** for confirmation
- **Decimal point (.)** as cancel/back
- **Plus (+) / Minus (-)** for quick mood adjustments (future)
- **Full keyboard** remains available for text entry when needed

### Input Device Configuration
- **Wired preferred** for reliability
- **USB numpad** as standalone device
- **Wireless acceptable** if battery life is good
- **Physical placement:** Near display, accessible while standing

## Data Persistence Requirements

### Database: SQLite
- **Location:** `data/moodbbs.db`
- **Backup strategy:** Simple file copy (user responsibility for now)
- **Schema version tracking:** For future migrations
- **ACID compliance:** Default SQLite guarantees sufficient

### Data Retention
- **Never delete user data** (archival over deletion)
- **Soft delete pattern** for hidden/removed items
- **Configurable event expiration** (default 24 hours for temporary modifiers)
- **Unlimited history** (disk space permitting)

### Required Tables (Implemented in MVP)
1. **mood_events** - Time-stamped mood modifiers
2. **quests** - Quest definitions and status
3. **quest_completions** - Historical quest completions
4. **user_traits** - RimWorld-style personality traits
5. **mood_snapshots** - Periodic mood state saves
6. **settings** - Key-value configuration

### Future Tables
1. **expedition_log** - Places visited, experiences logged
2. **memories** - Generated RimWorld-style memories
3. **quest_templates** - Reusable quest patterns
4. **mood_modifier_library** - Custom user-defined modifiers

## Performance Requirements

### Response Time
- **UI updates:** < 100ms from input to screen refresh
- **Database queries:** < 50ms for reads, < 100ms for writes
- **Boot time:** < 3 seconds to dashboard (after boot sequence)
- **Mood calculation:** < 10ms (multiple events + traits)

### Resource Usage
- **Memory:** < 50MB for main process
- **CPU:** Minimal (mostly idle)
- **Disk I/O:** Minimal (only on logging/completion)
- **Network:** None (except future API)

### Reliability
- **Uptime target:** 99.9% (allow for reboots/maintenance)
- **Data durability:** No data loss on clean shutdown
- **Crash recovery:** Graceful degradation, save state on exit
- **Database corruption:** Detect and alert (don't silently fail)

## Platform Requirements

### MVP Target
- **macOS** (primary development)
- **Terminal emulator:** Any modern terminal (iTerm2, Terminal.app)
- **Python version:** 3.8+
- **Dependencies:** Rich library, python-dateutil

### Future Targets
- **Raspberry Pi OS** (primary deployment target)
- **Linux** (Debian/Ubuntu)
- **Windows** (WSL or native, lower priority)

### Hardware Targets
- **Raspberry Pi 4** with 7" touchscreen (no touch needed)
- **Raspberry Pi Zero 2 W** with mini HDMI display
- **Any Linux box** with display output

## API Requirements (Future - v3)

### REST API
- **Framework:** Flask or FastAPI (TBD)
- **Port:** 8080 (configurable)
- **Protocol:** HTTP only (LAN-only, no TLS needed)
- **Format:** JSON

### Endpoints (Planned)
```
GET  /api/mood/current      - Current mood score and state
GET  /api/mood/history      - Historical mood data
POST /api/mood/event        - Log a mood event
GET  /api/quests/active     - Active quests
POST /api/quests/complete   - Complete a quest
GET  /api/traits            - User traits
```

### Security Model
- **Authentication:** None (LAN trust model)
- **Authorization:** None (single-user system)
- **CORS:** Disabled (LAN-only)
- **Rate limiting:** None initially
- **Validation:** Input validation on all POST endpoints

### Integration Use Cases
1. **Home Assistant** - Query mood, adjust lights/music
2. **Siri Shortcuts** - Voice queries ("What's my mood?")
3. **IFTTT/Zapier** - Trigger actions based on mood state
4. **Custom scripts** - Automated event logging

## UI Framework Requirements

### Rich Library
- **Version:** 13.0.0+
- **Features used:**
  - Console for output
  - Panel for bordered sections
  - Text for styled output
  - Tables for data display (future)
  - Layout for multi-section screens (future)
  - Live for real-time updates (future)

### Color Scheme
- **Mood indicators:**
  - Green: Positive mood (10+)
  - Yellow: Neutral mood (0-9)
  - Red: Negative mood (<0)
- **Accent colors:**
  - Cyan: Headers, titles, branding
  - Yellow: Quests, highlights
  - Blue: Info, secondary content
  - Dim: Timestamps, metadata

### ASCII Art Requirements
- **Boot screen:** MOOdBBS ASCII logo
- **Mood faces:** `:D`, `:)`, `:|`, `:(`, `D:`
- **Box drawing:** Unicode box characters for borders
- **Future:** Customizable ASCII art library

## Quest System Requirements

### Quest Data Model
```python
{
  "id": int,
  "title": str,              # "Walk to a bookstore"
  "description": str,        # Optional details
  "category": str,           # social, constitutional, creative, experiential
  "location": str,           # "Green Apple Books" or generic
  "xp_reward": int,          # Default 10
  "frequency": str,          # one-time, daily, weekly, monthly
  "status": str,             # active, completed, expired, hidden
  "created_at": timestamp,
  "due_at": timestamp,       # Optional deadline
  "completed_at": timestamp  # Null if not completed
}
```

### Quest Categories
1. **Social** - Friends, strangers, events, gatherings
2. **Constitutional** - Walks, bike rides, physical activity
3. **Creative** - Art, music, writing, making
4. **Experiential** - New places, novel experiences, exploration

### Quest Generation (Future)
- **Template-based** - Fill-in-the-blank patterns
- **User preferences** - Learn from completion patterns
- **Context-aware** - Weather, time of day, mood state
- **API-enhanced** - Yelp/events data for suggestions

### Quest Completion Flow
1. User selects quest from WanderMOO
2. User marks complete (number input)
3. System awards XP
4. System logs quest category
5. System applies base mood buff (+5)
6. System prompts for additional modifiers
7. User optionally logs pain, energy, etc.
8. Quest moves to completed state
9. If recurring, quest resets to active

## Mood Modifier Requirements

### Modifier Data Model
```python
{
  "event_type": str,         # ate_without_table, social_interaction
  "modifier": int,           # -3, +5, etc.
  "description": str,        # Human-readable description
  "duration_hours": int,     # How long it lasts (null = permanent)
  "category": str,           # stock, custom, quest
  "created_at": timestamp,
  "expires_at": timestamp    # Calculated from duration
}
```

### Stock RimWorld Modifiers (Phase 1)
- Ate without table: -3
- Had a fine meal: +5
- Social interaction: +8
- Completed a walk: +6
- Too long indoors: -5
- Saw something beautiful: +4

### Custom Modifiers (User-Defined)
- **Pain:** -x (user specifies severity 1-10)
- **Energized:** +y (user specifies level 1-10)
- **SF-specific:** "Fog rolled in", "BART delayed again"
- **Personal:** User can create any modifier with any value

### Modifier Library
- **Stock set** shipped with MOOdBBS
- **User additions** saved to database
- **Shareable** (export/import modifier sets, future)
- **Categorized** for easier selection

## Boot Sequence Requirements (v2)

### Dial-In Simulation
```
Dialing MOOdBBS...
CONNECT 56000 V.90

[ASCII art logo]

Welcome to MOOdBBS!

Last login: [timestamp]
```

### MOTD (Message of the Day)
- **Source:** Database setting or text file
- **Rotation:** Daily or random from pool
- **Content ideas:**
  - Inspirational quote
  - Local event reminder
  - Mood trend summary
  - System status

### Last Login Display
- **Show:** Date/time of last login
- **Show:** Mood score at last login
- **Show:** Quests completed since last login

## Configuration Requirements

### Settings Storage
- **Database table:** `settings` (key-value pairs)
- **Config file:** `config.ini` (optional override)
- **Environment variables:** Override for deployment

### Configurable Settings
- Display size mode (tiny/small/medium/large)
- Default quest XP value
- Default mood event duration (hours)
- MOTD content
- API enabled/disabled (future)
- API port (future)

### User-Editable Settings (via UI)
- Active traits (add/remove/toggle)
- Display preferences
- MOTD customization (future)

## Testing Requirements

### Unit Tests (Future)
- Database operations (CRUD for all tables)
- Mood calculation logic
- Quest completion flow
- Modifier expiration logic

### Integration Tests (Future)
- Full user flows (boot → log event → complete quest → exit)
- Database persistence across restarts
- API endpoints (when implemented)

### Manual Testing Checklist (MVP)
- ✓ Database creation and schema init
- ✓ Quest CRUD operations
- ✓ Mood event logging
- ✓ Mood calculation
- ✓ Trait management
- ✓ Data persistence across restarts
- ✓ UI navigation (menu, dashboard, screens)

## Deployment Requirements

### Development
- **Repository:** Git (local or GitHub)
- **Dependencies:** requirements.txt
- **Installation:** `pip install -r requirements.txt`
- **Launch:** `./run_moodbbs.sh` or `python src/main.py`

### Production (Raspberry Pi)
- **OS:** Raspberry Pi OS Lite (no desktop needed)
- **Auto-start:** systemd service
- **Display:** Console on HDMI output
- **Input:** USB numpad connected
- **Monitoring:** systemd status, optional external monitor

### Backup Strategy
- **Manual:** Copy `data/moodbbs.db` to backup location
- **Automated (future):** Daily cron job to backup database
- **Cloud sync (future):** Optionally sync to Dropbox/Drive

## Future Technical Considerations

### Expedition Log (v2)
- New table: `expedition_log`
- Fields: location, date, notes, photos (file paths)
- Integration with quest completion

### Memory System (v2)
- New table: `memories`
- Generated from mood events and quest completions
- RimWorld-style memory text generation
- Display in new "Memories" screen

### Advanced Quest System (v3)
- Quest chains (prerequisites)
- Quest templates with variables
- API-based quest generation
- Location-aware filtering

### Performance Monitoring
- Track slow queries (>100ms)
- Monitor memory usage over time
- Log database size growth
- Alert on anomalies
