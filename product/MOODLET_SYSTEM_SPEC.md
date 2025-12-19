# Moodlet System Specification

## Overview

The moodlet system is inspired by RimWorld's mood modifier system. Moodlets are temporary mood buffs/debuffs that apply when users complete quests or log events. They have specific durations and some have "backoff" mechanics where the mood boost gradually decreases over time.

## Core Concepts

### Quest-based vs Event-based Moodlets

- **Quest-based**: User actively pursues these by completing quests (e.g., "Go for a walk" → Energized)
- **Event-based**: Things that happen TO the user, logged manually (e.g., "Someone complimented me")

### Backoff Mechanic

High-intensity moodlets have a two-phase duration:
1. **Initial phase**: Full mood value for specified duration
2. **Backoff phase**: Reduced mood value for additional duration

Example: "Pumped" (+10, 10 hours) → "Workout Glow" (+5, 4 hours)

## Quest Categories & Moodlets

### 1. Exercise/Physical Activity

**Quest-based:**
```
[1] Refreshed        (+3, 2 hours)    "Got outside for a bit"
[2] Energized        (+5, 4 hours)    "Light workout put pep in my step"
[3] Pumped           (+10, 10h → +5, 4h)  "Muscles feel swole, bruh"
[4] Physically Spent (+15, 12h → +8, 12h) "Used everything I had!"
```

### 2. Social Interaction

**Quest-based:**
```
[1] Acknowledged     (+2, 2 hours)    "Complimented a stranger"
[2] Connected        (+5, 4 hours)    "Had a nice chat"
[3] Bonded           (+8, 8 hours)    "Meaningful conversation"
[4] Loved            (+12, 12h → +6, 12h) "Deep connection with friend/family"
```

**Event-based** (manually logged via QuickLog):
```
Positive:
- Gave someone a compliment    (+2, 2 hours)
- Remembered                   (+3, 2 hours)    "Someone remembered my name"
- Complimented                 (+4, 5 hours)    "Someone complimented me"
- Hugged                       (+5, 3 hours)    "Got a hug"
- Flirted (welcome)            (+5, 4 hours)    "Enjoyed mutual flirtation"
- Fun Encounter                (+6, 6 hours)    "Had unexpected fun encounter"
- Invited                      (+7, 8 hours)    "Invited to something"

Negative:
- Flirted (unwelcome)          (-5, 2 hours)    "Received unwanted advances"
- Dumped (casual)              (-8, 48h → -4, 48h)    "Casual relationship ended"
- Rejected                     (-10, 24h → -5, 12h)   "Turned down (job, date, etc.)"
- Friend breakup               (-12, 96h → -6, 72h)   "Lost a close friendship"
- Dumped (serious)             (-15, 72h → -8, 120h)  "Significant relationship ended"
- Dumped (long-term)           (-25, 168h → -12, 336h) "Long-term relationship ended"
```

### 3. Creative/Learning

**Quest-based:**
```
[1] Engaged          (+3, 3 hours)    "Tried something new"
[2] Accomplished     (+6, 6 hours)    "Made progress on a project"
[3] Proud            (+9, 10 hours)   "Created something meaningful"
[4] Brilliant        (+12, 12h → +6, 8h) "Had a breakthrough!"
```

**Event-based:**
```
- Learned something interesting  (+4, 4 hours)
- Solved a tricky problem       (+6, 6 hours)
- Someone praised my work       (+8, 8 hours)
- Finished a project            (+10, 12 hours)
```

### 4. Exploration/Discovery

**Quest-based:**
```
[1] Curious          (+3, 3 hours)    "Explored somewhere nearby"
[2] Adventurous      (+6, 6 hours)    "Discovered a new place"
[3] Amazed           (+9, 8 hours)    "Found something unexpected"
[4] Wonder-struck    (+12, 10h → +6, 6h) "Saw something breathtaking"
```

### 5. Food/Culinary

**Quest-based:**
```
[1] Satisfied        (+3, 2 hours)    "Ate a decent meal"
[2] Delighted        (+5, 4 hours)    "Had something tasty"
[3] Luxuriated       (+8, 6 hours)    "Enjoyed a fine meal"
[4] Blissful         (+10, 8h → +5, 4h) "Ate something amazing"
```

**Event-based** (manually logged via QuickLog):
```
Positive:
- Ate a fine meal                (+6, 4 hours)
- Ate a lavish meal              (+9, 6 hours)

Alcohol (with negative backoff after 12h):
- Had a drink                    (+4, 2h → -2, 12h)
- Had a few drinks               (+6, 3h → -3, 12h)
- Got tipsy                      (+8, 4h → -4, 12h)
- Whiskey warmth                 (+4, 1h → -2, 12h)

Negative:
- Ate without table              (-3, 2 hours)
- Skipped a meal                 (-4, 4 hours)
- Ate nutrient paste             (-5, 3 hours)
```

### 6. Rest/Relaxation

**Quest-based:**
```
[1] Calmer           (+3, 3 hours)    "Took a break"
[2] Recharged        (+5, 5 hours)    "Rested properly"
[3] Restored         (+8, 8 hours)    "Got good sleep"
[4] Renewed          (+10, 12h → +5, 6h) "Deeply rested"
```

### 7. Self-Care

**Event-based** (manually logged via QuickLog):
```
- Took a hot shower              (+3, 2 hours)    "Clean and refreshed"
- Took a bath                    (+5, 3 hours)    "Relaxed and soothed"
- Got my nails done              (+5, 4h → +3, 120h)  "Nails looking good"
- Did my skin care routine       (+5, 12 hours)   "Skin feels refreshed"
- Got a great haircut            (+10, 8h → +4, 120h) "Fresh haircut feels amazing"
- Watching comfort TV/movie      (+10, 1 hour)    "Enjoying comfort media"
```

**Note:** Haircut and nail moodlets have extended backoff periods (120h = 5 days) reflecting their longer-lasting effects.

### 8. Culture/Art

**Quest-based:**
```
[1] Inspired         (+4, 4 hours)    "Saw something artistic"
[2] Moved            (+6, 6 hours)    "Experienced beautiful art"
[3] Transported      (+9, 8 hours)    "Lost in a performance/exhibit"
[4] Transcendent     (+12, 10h → +6, 8h) "Art changed my perspective"
```

### 9. System

**System-applied** (automatic):
```
- Joined MOOdBBS!    (+5, 24 hours)   "Welcome bonus on first login"
```

## Design Principles

1. **Tiny boosts exist** (2-3 points, 2-3 hours) for micro-actions like "complimented a stranger"
2. **Progressive scaling**: Each tier roughly doubles in magnitude and duration
3. **Backoff mechanic** reserved for highest tier (exhausting/transformative experiences)
4. **Event-based vs Quest-based** distinction maintained
5. **Specificity in descriptions** helps users understand what caused the feeling

## QuickLog Interface

The QuickLog screen (renamed from LogAction) provides a categorized browser for manually logging moodlets:

1. **Category Selection**: User chooses from available categories (Creative, Food, Self-Care, Social)
2. **Moodlet Browser**: Shows all moodlets in selected category with mood value and duration
3. **One-Press Application**: User selects number to instantly apply moodlet
4. **Custom Moodlets**: Option to create custom moodlet (LLM suggestions coming soon)

### QuickLog Flow
```
┌─────────────────────────────────────────────┐
│              QuickLog Categories             │
├─────────────────────────────────────────────┤
│ [1] Creative (4 moodlets)                   │
│ [2] Food (9 moodlets)                       │
│ [3] Self Care (6 moodlets)                  │
│ [4] Social (13 moodlets)                    │
│ [c] Create custom moodlet                   │
└─────────────────────────────────────────────┘

User selects category, then sees:

┌─────────────────────────────────────────────┐
│              Social Moodlets                 │
├─────────────────────────────────────────────┤
│ [1] +7 Invited (8h)                         │
│ [2] +6 Fun Encounter (6h)                   │
│ [3] +5 Hugged (3h)                          │
│ [4] +5 Flirted (welcome) (4h)               │
│ ... and 9 more                              │
└─────────────────────────────────────────────┘
```

## Quest Completion Flow

When completing a quest, users are shown a **category-specific moodlet menu** (skippable):

```
┌─────────────────────────────────────────────┐
│ Quest Completed: Walk to Alta Plaza Park    │
│ +12 XP earned!                              │
├─────────────────────────────────────────────┤
│ How do you feel after this quest?           │
│                                             │
│ [1] Refreshed      (+3, 2 hours)           │
│ [2] Energized      (+5, 4 hours)           │
│ [3] Pumped         (+10, 10 hours)         │
│ [4] Physically Spent (+15, 12 hours)       │
│ [s] Skip (use default)                     │
└─────────────────────────────────────────────┘
```

If skipped, system applies default moodlet for that quest type.

## Database Schema

### Moodlets Table (pre-populated)

```sql
CREATE TABLE moodlets (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,  -- 'exercise', 'social', 'creative', 'exploration', 'food', 'rest', 'selfcare', 'culture', 'system'
  mood_value INTEGER NOT NULL,
  duration_hours INTEGER NOT NULL,
  backoff_value INTEGER,  -- NULL if no backoff (can be negative for hangovers)
  backoff_duration_hours INTEGER,  -- NULL if no backoff
  description TEXT,
  is_quest_based BOOLEAN DEFAULT 1  -- 1 for quest-based, 0 for event-based
);
```

### Active Moodlets Table (instances)

```sql
CREATE TABLE active_moodlets (
  id INTEGER PRIMARY KEY,
  user_id INTEGER DEFAULT 1,
  moodlet_id INTEGER REFERENCES moodlets(id),
  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NOT NULL,
  backoff_expires_at TIMESTAMP,  -- NULL if no backoff or not in backoff yet
  is_in_backoff BOOLEAN DEFAULT 0,
  source_quest_id INTEGER,  -- NULL if event-based
  source_event_id INTEGER   -- NULL if quest-based
);
```

## Mood Calculation

Current mood score is calculated as:
```
mood_score = base_mood + Σ(active_moodlets) + Σ(trait_modifiers)
```

Where `active_moodlets` are all non-expired moodlets, using either full value or backoff value depending on current time.

## Implementation Notes

### Moodlet Expiration

- Check `expires_at` vs current time
- If expired and has backoff, transition to backoff phase:
  - Set `is_in_backoff = 1`
  - Set `expires_at = backoff_expires_at`
  - Mood calculation uses `backoff_value` instead of `mood_value`
- If expired and no backoff (or backoff expired), remove from active moodlets

### Default Moodlets by Quest Category

When user skips moodlet selection, apply default:
- **Exercise**: Energized (+5, 4 hours)
- **Social**: Connected (+5, 4 hours)
- **Creative**: Accomplished (+6, 6 hours)
- **Exploration**: Adventurous (+6, 6 hours)
- **Food**: Delighted (+5, 4 hours)
- **Rest**: Recharged (+5, 5 hours)
- **Culture**: Moved (+6, 6 hours)

**Note:** Self-care category is event-based only (manually logged), not quest-based.

### Moodlet Stacking

Multiple instances of the same moodlet CAN stack (e.g., two walks give two "Energized" buffs). This encourages repeated positive actions.

## Future Enhancements

- **Planned breaks**: Streak system allows "planned day off" without resetting
- **Negative moodlets**: Expand RimWorld-style debuffs
- **Weather-dependent moodlets**: "Walked in rain" gets bonus moodlet
- **Personal records**: Breaking personal best triggers special moodlet
- **Combo moodlets**: Completing multiple quests in one day triggers special buff
