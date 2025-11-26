# Quest System Specification

## Overview

The quest system turns real-world activities into game-like goals with XP rewards and mood buffs. Quests encourage exploration, social interaction, physical activity, and creative pursuits.

## Core Principles

1. **Auto-renewal** - Expired quests automatically renew (unless hidden)
2. **User control** - "Not now" (snooze) and "Never again" (hide) options
3. **Real constraints** - Time pressure comes from reality (closing times, events)
4. **Difficulty = Effort** - Harder quests give more XP
5. **Track but don't assume** - Log location data, but don't auto-predict preferences
6. **User + System creation** - Both manual and generated quests

## Quest States

```
┌──────────┐
│ Template │
└────┬─────┘
     │ instantiate
     ▼
┌──────────┐    snooze    ┌─────────┐   auto-return  ┌────────┐
│  Active  ├─────────────►│ Snoozed ├───────────────►│ Active │
└────┬─────┘              └─────────┘                └────────┘
     │
     │ complete/expire
     ▼
┌─────────────────┐   cooldown elapsed   ┌────────┐
│ Pending Renewal ├─────────────────────►│ Active │
└────┬────────────┘                      └────────┘
     │
     │ "never again"
     ▼
┌────────┐
│ Hidden │
└────────┘
```

### State Definitions

- **Active**: Available for completion, shows in quest list
- **Snoozed**: User said "not now", returns after configured days (default 7)
- **Completed**: User finished the quest, awarded XP
- **Pending Renewal**: Waiting for cooldown period before renewing
- **Hidden**: User said "never show again", permanently filtered

## Quest Difficulty

Difficulty is category-specific and affects XP rewards.

### Constitutional Difficulty

Based on physical effort:
- **Easy** (5-10 XP): Short walk, < 30 min, flat terrain
- **Medium** (15-20 XP): Moderate walk/bike, 30-90 min, some hills
- **Hard** (25-35 XP): Long bike ride, 2-3 hours, significant elevation
- **Extreme** (40-50 XP): All-day adventure, major physical challenge

Examples:
```
Easy: "Walk to nearby coffee shop" (10 min walk)
Medium: "Bike to Golden Gate Park" (45 min, some hills)
Hard: "Bike up Hawk Hill backside" (2 hrs, 1200 ft elevation)
Extreme: "Bike to Point Reyes" (8 hrs, 60 miles)
```

### Social Difficulty

Based on coordination complexity and group size:
- **Easy** (5-10 XP): 1-2 people, low coordination
- **Medium** (15-20 XP): 3-5 people, moderate coordination
- **Hard** (25-35 XP): 6-10 people, high coordination or hosting
- **Extreme** (40-50 XP): Large party, complex coordination

Examples:
```
Easy: "Coffee with one friend"
Medium: "Dinner with 4 friends"
Hard: "Host dinner party for 8"
Extreme: "Organize 20-person gathering"
```

### Creative Difficulty

Based on time commitment and skill level:
- **Easy** (5-10 XP): Visit museum, attend performance (passive)
- **Medium** (15-20 XP): Sketch at park, write at cafe (active)
- **Hard** (25-35 XP): Complete art project, write story (sustained effort)
- **Extreme** (40-50 XP): Major creative work, portfolio piece

### Experiential Difficulty

Based on novelty and adventure level:
- **Easy** (5-10 XP): New cafe in familiar neighborhood
- **Medium** (15-20 XP): New neighborhood exploration
- **Hard** (25-35 XP): Unfamiliar part of city, requires navigation
- **Extreme** (40-50 XP): Major adventure, requires planning

## Time Constraints

Quests can have real-world deadlines:

### Constraint Types

1. **closing_time** - Location closes (museums, shops)
2. **event_time** - One-time event (concerts, readings, parties)
3. **natural_timing** - Sunset, golden hour, seasonal
4. **expiration** - User-defined deadline

### UI Display

```
Active Quests:
  1. Visit SFMOMA [25 XP] ⏰ Closes at 4pm (3h left)
  2. Poetry at City Lights [15 XP] 📅 Tonight 7pm
  3. Sunset at Twin Peaks [10 XP] 🌅 5:15pm today
  4. Walk to bookstore [10 XP]
```

## Quest Snoozing ("Not Now")

User can defer a quest with optional feedback.

### Flow

```
User: snooze 2
System: Quest snoozed: "Bike up Hawk Hill"

Why not now? (Enter to skip)
  1. Weather
  2. Don't have time
  3. Not in the mood
  4. Other (specify)

Select (or Enter): 1

System: Noted! Snoozed for 7 days.

Feedback saved:
  Quest: Bike up Hawk Hill
  Reason: Weather
  Date: 2025-12-15
  Weather: Rainy, 45°F
```

**Alternative with custom text:**
```
Select (or Enter): 4
Other reason: It's too cold and rainy for biking

System: Noted! Snoozed for 7 days.
```

### Snooze Data

```python
@dataclass
class QuestSnooze:
    quest_id: int
    snoozed_at: datetime
    return_at: datetime  # Auto-returns to Active
    reason: Optional[str]  # User explanation
    context: Dict  # Weather, mood, day of week
```

### Future Use

Snooze reasons can inform quest generation:
- "Too cold" + bike quest → Don't suggest bike quests in winter
- "Too many people" + party → Prefer smaller gatherings
- "Too far" + location → Suggest closer alternatives

**Important:** Don't build recommendation system yet. Just collect data.

## Quest Renewal System

Quests auto-renew after completion/expiration based on renewal policy.

### Renewal Types

**Daily Renewal (cooldown: 1 day)**
- Most quests fall into this category
- Casual activities, museums, easy social
- Examples: "Visit Cal Academy", "Walk to bookstore"

**Weekly Renewal (cooldown: 7 days)**
- Moderate challenges
- Regular events
- Examples: "Bike up Hawk Hill", "Weekly brunch group"

**Monthly Renewal (cooldown: 30 days)**
- Hard challenges, major events
- Once-a-month activities
- Examples: "Host dinner party", "Poetry night (first Friday)"

**Seasonal Renewal (cooldown: 365 days, active_months)**
- Weather/season dependent
- Annual events
- Examples: "Point Reyes wildflowers (spring only)"

**Never Renewal**
- One-time events
- User set "never show again"
- Moves to Hidden state

### Renewal Flow

```
Quest completed/expired
  ↓
Check renewal_policy
  ↓
Calculate next_eligible_renewal = now + cooldown_days
  ↓
Set status = "pending_renewal"
  ↓
Daily background job checks pending renewals
  ↓
If next_eligible_renewal <= now:
  ↓
  Check seasonal restrictions (if any)
  ↓
  Check if room in active quests
  ↓
  If yes: status = "active"
```

### Template Example

```yaml
- id: visit_cal_academy
  title: "Visit California Academy of Sciences"
  category: experiential
  difficulty: easy
  base_xp: 10
  renewal_policy:
    type: daily
    cooldown_days: 1
  tags: [museum, indoors]

- id: bike_hawk_hill
  title: "Bike up Hawk Hill"
  category: constitutional
  difficulty: hard
  base_xp: 30
  renewal_policy:
    type: weekly
    cooldown_days: 7
  tags: [bike, challenge]

- id: point_reyes_wildflowers
  title: "Bike to Point Reyes for wildflowers"
  category: experiential
  difficulty: extreme
  base_xp: 50
  renewal_policy:
    type: seasonal
    cooldown_days: 365
    active_months: [3, 4, 5]  # Spring
  tags: [bike, nature, seasonal]
```

### UI Display

```
Active Quests (3/3):
  1. Visit Cal Academy [10 XP]
  2. Walk to bookstore [10 XP]
  3. Coffee with friend [15 XP]

Pending Renewal (5):
  • Bike Hawk Hill (renews in 5 days)
  • Poetry night Coit (renews Dec 6)
  • Host dinner party (renews in 23 days)
  • Point Reyes wildflowers (renews next spring)
  • SFMOMA visit (renews tomorrow)
```

## Active Quest Limit

**Default:** 3 active quests max
**Configurable:** User can change in Settings

### Behavior at Limit

- Cannot add new quest without freeing a slot
- Free slots by: completing, snoozing, or hiding
- Or: increase limit in settings temporarily
- Pending renewal quests wait for open slots

## Location Tracking

Track where user goes and when, but don't assume preferences.

### San Francisco Neighborhoods

Hardcoded list of SF neighborhoods in `config/sf_neighborhoods.yaml`.

Categories: downtown, central, west, north, east, southeast, south, waterfront, outside

Examples:
- Downtown: Financial District, Union Square, Chinatown, North Beach
- Central: Mission, Castro, Haight, Hayes Valley, NOPA
- West: Richmond, Sunset, Golden Gate Park
- North: Marina, Pacific Heights, Presidio
- Outside: Marin Headlands, Point Reyes, Sausalito

### Location Visit Data

```python
@dataclass
class LocationVisit:
    location_name: str
    address: Optional[str]
    neighborhood: str  # From config/sf_neighborhoods.yaml
    coordinates: Optional[Tuple[float, float]]
    first_visit: datetime
    last_visit: datetime
    visit_count: int
    quest_completions: List[int]  # Quest IDs
    avg_duration_minutes: int
    categories: Set[str]  # social, constitutional, etc.
```

### Exploration Tracking

```python
@dataclass
class ExplorationStats:
    neighborhoods_visited: Set[str]
    neighborhoods_never_visited: Set[str]
    neighborhood_visit_counts: Dict[str, int]
    category_durations: Dict[str, List[int]]  # Minutes per category
    completion_times: Dict[int, datetime]  # When quests done
```

### Quest Generation Heuristic (v2)

**Goal:** Encourage exploration of new areas, not predict preferences.

```
Simple algorithm:
1. Get list of SF neighborhoods never visited
2. Find quest templates for those neighborhoods
3. Randomly select one
4. Generate quest instance

DO NOT:
- Try to predict which quests user will like
- Build recommendation engine
- Assume past behavior = future preference
```

## User-Created Quests

Users can create custom quests for personal events/goals.

### Creation Flow (Shell)

```
moodbbs> create quest

Title: First Friday at SOMArts
Description: Opening reception, free wine, check out installation
Category:
  1. Social
  2. Constitutional
  3. Creative
  4. Experiential
Select: 3

Location: SOMArts Cultural Center, 2nd & Bryant

XP reward (default 15): 20

Deadline (optional, YYYY-MM-DD HH:MM): 2025-12-01 19:00

Difficulty:
  1. Easy (5-10 XP)
  2. Medium (15-20 XP)
  3. Hard (25-35 XP)
  4. Extreme (40-50 XP)
Select: 1

Quest created! Added to active quests.
```

### Creation Flow (TUI)

Interactive form with same fields, numpad navigation.

## LLM-Powered Quest Creation

### Overview

MOOdBBS uses an LLM to parse natural language quest descriptions, reducing friction in quest creation. The LLM extracts structured data from user input like "Visit Cal Academy on a weekday" or "First Friday poetry at Coit Tower".

### Architecture: Base XP + User Adjustments

**Core Principle:** The LLM sets **base difficulty XP** for the activity type itself, then the **application layer applies user-specific adjustments** based on actual profile data (memberships, location, etc.).

This two-layer approach ensures:
1. **Portability** - Quest base XP is the same for all users regardless of location/circumstances
2. **No assumptions** - LLM doesn't guess whether a user has a membership or lives nearby
3. **Personalization** - System applies adjustments only when user profile data exists
4. **Transparency** - UI shows both base XP and adjustment reason

### Base XP Guidelines

The LLM assigns base XP based on activity type:

```
Simple daily activities (walk, journal):         10 XP
Social meetups, short outings:                   15-20 XP
Museum visits, attractions, events:              25-30 XP
Complex multi-step activities:                   35-45 XP
```

Examples of base XP (same for all users):
- "Daily morning walk": 10 XP
- "Coffee with a friend": 15 XP
- "First Friday poetry reading": 20 XP
- "Visit Cal Academy": 25 XP
- "Visit SFMOMA": 25 XP
- "Host dinner party for 8": 35 XP

### User-Specific Adjustments

After LLM parsing, the application layer applies adjustments based on actual user profile:

#### Membership Adjustments

User memberships serve three purposes:
1. **Low friction quests** - No admission cost means easier to "just go"
2. **Interest indicators** - Shows what types of venues the user enjoys
3. **Weekday quest recommendations** - Easy to suggest as quick weekday outings

If user has a membership that matches the quest location:
- **XP multiplier:** 0.7 (30% reduction reflects lower friction, not lower value)
- **Minimum XP:** 5 (even with membership, still worth doing)
- **Display:** Shows original and adjusted XP with positive framing

Example:
```
User profile: memberships: ["Cal Academy", "SFMOMA"]

Quest: "Visit Cal Academy"
- Base XP: 25
- Adjusted XP: 17 (Easy access! Adjusted from 25 - no admission cost with Cal Academy membership)
```

#### Distance Adjustments (Future)
When user home location is configured:
- Nearby locations: No adjustment
- Cross-city travel: +5 XP
- Out of SF proper: +10 XP

### What LLM Context Receives

The LLM receives **minimal** user context for reference only:
- Home neighborhood (e.g., "User lives in Inner Richmond")
- Transportation preferences (e.g., "Prefers walking, transit")

**Does NOT receive:**
- Memberships (handled at application layer)
- Exact address
- Past quest history

### Implementation Details

#### LLM Prompt Guidelines
```
Set XP based on the ACTIVITY ITSELF, not user circumstances.
The system will adjust for user memberships/location later.
```

#### Application Layer (screens.py)
```python
# After LLM parsing
base_xp = quest_data['xp_reward']
adjusted_xp = base_xp

user_profile = self.engine.db.get_user_profile()
if user_profile.memberships:
    # Check if quest location matches any membership
    for membership in user_profile.memberships:
        if membership.lower() in quest_title.lower():
            adjusted_xp = max(5, int(base_xp * 0.7))
            # Show adjustment note in UI
```

#### UI Display
```
Parsed Quest:
  Title: Visit California Academy of Sciences
  Description: Go to the Cal Academy in Golden Gate Park
  Category: experiential
  XP Reward: 17
    (Reduced from 25 - you have Cal Academy membership)
  Renewal: seasonal
  Constraint: 10:00-17:00
  Time: Opens 10am, closes 5pm

How often would you like to do this?
  1. One-time only
  2. Daily
  3. Weekly
  4. Monthly
  5. Seasonal (every 3 months)
  6. Use suggested (seasonal)

Select (1-6):
```

### Benefits of This Architecture

1. **Works for new users** - A user in NYC creating SF quests gets accurate base XP
2. **No false assumptions** - LLM doesn't guess memberships based on quest type
3. **Transparent adjustments** - User sees why XP changed
4. **Portable quest data** - Base difficulty is consistent across all users
5. **Future-proof** - Easy to add new adjustment types (distance, weather, etc.)

### Parsed Fields

The LLM extracts these fields from natural language:

```python
{
    "title": str,              # Short quest title
    "description": str,        # What to do
    "category": str,           # social, constitutional, creative, experiential
    "xp_reward": int,          # Base difficulty XP
    "renewal_type": str,       # daily, weekly, monthly, seasonal, or null
    "constraint_type": str,    # day_of_week, day_of_month, time_of_day, or null
    "constraint_note": str,    # Constraint details (e.g., "first_friday", "10:00-17:00")
    "time_note": str          # Operating hours (e.g., "Open 10am-5pm, closed Wednesdays")
}
```

### LLM Knowledge Integration

The LLM uses its knowledge of SF attractions to automatically add:
- **Operating hours** - Museums close at 5pm, cafes open at 7am
- **Time constraints** - "First Friday" becomes `constraint_type: "day_of_month"`, `constraint_note: "first_friday"`
- **Renewal patterns** - Museums suggest "seasonal", daily activities suggest "daily"

Example:
```
User input: "Visit SFMOMA"
LLM output:
{
  "title": "Visit SFMOMA",
  "description": "Go to the SF Museum of Modern Art",
  "category": "experiential",
  "xp_reward": 25,
  "renewal_type": "seasonal",
  "constraint_type": "time_of_day",
  "constraint_note": "10:00-17:00",
  "time_note": "Open 10am-5pm, closed Wednesdays"
}
```

### User Override

After parsing, user can:
1. **Choose renewal frequency** - Override LLM suggestion (e.g., change "daily" to "monthly")
2. **Confirm or cancel** - Review all parsed data before creating quest
3. **Fall back to manual** - If LLM parsing fails, use full manual form

### Future Enhancements

- **Location-aware distance** - Adjust XP based on travel distance from user's home
- **Weather-aware timing** - Suggest indoor quests on rainy days
- **Event integration** - Parse event dates from description
- **Multi-step quests** - Break complex activities into sub-quests

## Quest Templates

Templates are stored in `config/quest_templates.yaml` for easy editing.

### Template Structure

```yaml
templates:
  - id: walk_to_bookstore
    title: "Walk to a bookstore"
    description: "Choose any bookstore in SF"
    category: constitutional
    difficulty: easy
    base_xp: 10
    optionality: high
    suggested_locations:
      - name: Green Apple Books
        neighborhood: Richmond
        distance: short
      - name: City Lights
        neighborhood: North Beach
        distance: medium
      - name: Dog Eared Books
        neighborhood: Mission
        distance: medium
    tags: [outdoors, exercise, literacy]

  - id: bike_hawk_hill
    title: "Bike up backside of Hawk Hill"
    description: "Challenging climb with amazing views at the top"
    category: constitutional
    difficulty: hard
    base_xp: 30
    optionality: low
    duration_estimate: "2 hours"
    suggested_locations:
      - name: Hawk Hill
        neighborhood: Marin Headlands
        distance: far
    difficulty_factors:
      elevation_gain: 1200  # feet
      distance: 10  # miles roundtrip
    tags: [outdoors, exercise, challenge, views]
```

## Quest Completion Flow

### Completion Command

```
moodbbs> complete 2

Quest completed! +15 XP
Total XP: 145

Mood buffs applied:
  +5  Quest completed (base)
  +6  Constitutional activity (category bonus)

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

Total mood change: :) [+12] → :D [+27]
```

### Completion Data

```python
@dataclass
class QuestCompletion:
    id: int
    quest_id: int
    completed_at: datetime
    location_visited: str  # Actual location user went
    duration_minutes: Optional[int]
    notes: str
    mood_modifiers_logged: List[Tuple[str, int]]
    xp_awarded: int
```

## Quest Data Models

### Quest Template

```python
@dataclass
class QuestTemplate:
    id: str
    title: str
    description: str
    category: str  # social, constitutional, creative, experiential
    difficulty: str  # easy, medium, hard, extreme
    base_xp: int
    optionality: str  # high, medium, low
    suggested_locations: List[Dict]
    duration_estimate: Optional[str]
    tags: List[str]
    difficulty_factors: Optional[Dict]
```

### Renewal Policy

```python
@dataclass
class RenewalPolicy:
    renewal_type: str  # daily, weekly, monthly, seasonal, never
    cooldown_days: int  # Minimum days before renewal
    max_active_instances: int = 1  # How many can be active at once
    active_months: Optional[List[int]] = None  # For seasonal [3,4,5]
    schedule: Optional[str] = None  # "first_friday", etc.
```

### Quest Instance

```python
@dataclass
class Quest:
    id: int
    template_id: Optional[str]  # None if user-created
    title: str
    description: str
    category: str
    difficulty: str
    location: str
    xp_reward: int
    status: str  # active, snoozed, completed, pending_renewal, hidden
    renewal_policy: Optional[RenewalPolicy]
    next_eligible_renewal: Optional[datetime]
    renewal_count: int  # How many times renewed
    created_at: datetime
    due_at: Optional[datetime]
    constraint_type: Optional[str]  # closing_time, event_time, etc.
    constraint_note: Optional[str]
    completed_at: Optional[datetime]
```

### Quest Snooze

```python
@dataclass
class QuestSnooze:
    id: int
    quest_id: int
    snoozed_at: datetime
    return_at: datetime
    reason: Optional[str]  # "weather", "no_time", "not_in_mood", or custom text
    reason_category: str  # "weather", "time", "mood", "other"
    context: Dict  # weather, mood_score, day_of_week, etc.
```

**Reason categories:**
- `weather`: User cited weather as reason
- `time`: "Don't have time"
- `mood`: "Not in the mood"
- `other`: Custom text provided

## Settings

Quest-related user settings:

```python
{
  "max_active_quests": 3,           # Configurable
  "auto_renew_expired": True,        # Auto-renew expired quests
  "snooze_default_days": 7,          # Default snooze duration
  "quest_generation_enabled": True,  # System generates quests
  "generation_frequency": "weekly"   # How often to generate
}
```

## Implementation Priority (v1)

### Must Have
- [x] Quest states (active, completed, expired, hidden, snoozed)
- [ ] Quest difficulty system with XP scaling
- [ ] Auto-renewal of expired quests
- [ ] "Not now" snooze with optional feedback
- [ ] "Never again" hide functionality
- [ ] User-created quests
- [ ] Quest completion with mood logging
- [ ] Active quest limit (configurable)
- [ ] Basic location tracking

### Nice to Have (v2)
- [ ] Quest templates in YAML
- [ ] Template-based generation
- [ ] Exploration stats (neighborhoods visited)
- [ ] Snooze reason analysis
- [ ] Time constraint display (countdown timers)
- [ ] Quest difficulty auto-calculation (for bike routes)

### Future (v3)
- [ ] Unexplored area suggestions
- [ ] Weather-aware quest suggestions
- [ ] Event API integration
- [ ] Quest chains
- [ ] Achievement system

## Weather Integration (Future)

### Overview
Integrate real-time weather data to create urgency and improve quest suggestions.

### Compelling Use Cases
**Hourly rain predictions** create natural urgency:
- "Better take that 30 min bike ride NOW before the wind picks up!"
- "Rain starts in 2 hours - perfect window for Ocean Beach walk"
- "Clear skies for next 4 hours - ideal for Hawk Hill attempt"

### Data Sources (v3)
- **Hourly forecasts**: Rain predictions, wind speed, temperature
- **Current conditions**: Real-time weather updates
- **Neighborhood-specific** (v2+): Marina vs. Mission microclimate differences

### Quest Suggestion Integration
```
System notices:
- Current: Sunny, 65°F, light breeze
- Next 3 hours: Same conditions
- Hour 4-6: Rain 80% likely, wind 20mph

Suggestion: "Perfect weather window for constitutional quest!"
  → Bike to Golden Gate Park [20 XP]
     ⚡ Weather window: 3 hours before rain

Active quest updated:
  → Walk to Ocean Beach [15 XP]
     🌧️ Rain starts in 2h - go now or snooze?
```

### Weather Context in Snooze Data
Already capturing weather context when user snoozes:
```python
{
  "reason": "weather",
  "context": {
    "weather": "Rainy, 45°F, 15mph wind",
    "conditions": ["rain", "cold", "windy"]
  }
}
```

Future: Learn patterns like "User doesn't bike when <50°F" or "User avoids rain"

### Implementation Priority
- **v3**: Basic weather API integration (citywide)
- **v4**: Hourly forecasts for urgency messaging
- **v5**: Neighborhood-specific microclimates

### Technical Notes
- APIs: OpenWeather, Weather.gov, or similar
- Update frequency: Every 30-60 minutes
- Cache forecasts to avoid rate limits
- Display weather icons in quest list (☀️ 🌧️ 💨 ❄️)

## Open Questions

1. **Snooze duration:** Should different quest types have different default snooze durations?
2. **Auto-generation frequency:** How often should system suggest new quests?
3. **XP progression:** Should XP unlock anything, or purely cosmetic?
4. **Quest retirement:** Should completed quests ever be deleted, or keep forever?
5. **Difficulty calculation:** For bike routes, should we integrate with mapping APIs for elevation data?
