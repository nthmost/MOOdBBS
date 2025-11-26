# MOOdBBS Product Vision

## Overview

MOOdBBS is a RimWorld-inspired mood tracking system with real-world quest mechanics, presented through a 90s BBS aesthetic. It transforms daily life into a game-like experience where mood modifiers and personal quests create a non-judgmental framework for self-awareness and exploration.

## Core Philosophy

**"Turning the real world into an ARG"** - MOOdBBS treats everyday life as an augmented reality game, making self-care and exploration feel like gameplay rather than obligation.

**Non-judgmental reflection** - The system simply reflects back numerical mood data without judgment. Computers don't judge; they show patterns. This creates safe space for honest mood tracking.

**Near-zero friction** - Most interactions should be quick (10 seconds or less) with minimal cognitive load. The numpad interface enables this.

## Target User

**Primary user:** The creator (you)
**Secondary users:** Other individuals who:
- Enjoy gamification of self-improvement
- Appreciate retro aesthetics
- Want simple, visual mood tracking
- Live in urban environments with exploration opportunities
- Value optionality in goal-setting

## Physical Setup

### Display Configuration
- **Multiple screen sizes supported** (like claude-monitor's display modes)
- **Primary deployment:** Wall-mounted display in kitchen near mail area
- **Interaction style:** Walk-up, quick interactions throughout the day
- **Always-on dashboard** showing current mood, active quests, recent events

### Input Devices
- **Phase 1 (Current):** Full keyboard for learning and customization
- **Phase 2 (Future):** Primarily numpad with full keyboard as fallback
- **Wired preferred** for reliability and simplicity
- **Placement:** Accessible but not obstructive

## Use Cases

### Morning Check-in
- User wakes up in bad (or good) mood
- Walks to MOOdBBS dashboard
- Views recent mood events from past week
- Understands current mood score context

### Event Logging
- Something happens during the day (social interaction, meal, pain, etc.)
- User quickly logs it (10 seconds)
- Mood score updates immediately
- User returns to activity

### Post-Quest Logging
- User returns from walk/bike ride/exploration
- Marks quest as complete
- System awards XP and mood buff
- System prompts for additional mood modifiers
- User optionally logs extra events (energized, pain, etc.)

### Weekly Review
- User checks MoodStats to see patterns
- Reviews completed quests
- Adjusts active quests or traits as needed

## The RimWorld Connection

### Why RimWorld?
- **Simple yet powerful** mood system
- **Recognizable modifiers** that match real life
- **Arbitrary but relatable** (wife dies = breakdown, ate without table = minor debuff)
- **User plays RimWorld extensively** and likes the mental model

### Implementation Approach
- **Start with RimWorld stock modifiers** (as close as possible)
- **Support custom modifiers** from day one
- **User-extensible** system for adding new buffs/debuffs
- **Keep the spirit** while adapting to real-world contexts

### Mood Modifiers Examples
- Standard RimWorld: "Ate without table (-3)", "Beautiful environment (+4)"
- SF-flavored: "Fog rolled in (+2)", "BART delayed again (-3)"
- Custom user: "Pain" (-x based on severity), "Energized" (+y based on activity)

## Quest System Design

### Quest Categories
Initial categories for tracking:
1. **Social** - Interactions with friends, strangers, events
2. **Constitutional** - Physical activities good for overall health (walks, bike rides)
3. **Creative** - Art, writing, making things
4. **Experiential** - Novel experiences, new places

### Quest Optionality
Quests provide **flexible goals** rather than rigid requirements:
- "Take a walk to a bookstore" (not "Walk to City Lights at 3pm")
- "Climb a tree" (any tree, any height)
- "Bike to an art museum" (user chooses which, when, how far)

Over time, quests become more specific as user learns preferences:
- "Walk to Green Apple Books" (short walk, close by)
- "Walk to City Lights Bookstore" (long walk, requires late afternoon/evening)

### Quest Types
- **One-time events** - "Go to poetry night on Coit Tower" (first Friday)
- **Recurring quests** - Daily/weekly goals like "Take 3 walks this week"
- **Recyclable quests** - Can be reused if not completed, no penalty

### Quest Generation
**Phase 1:** Manual entry with categories (user and Claude collaborate)
**Phase 2:** Learn patterns from completed quests
**Phase 3:** API integration (Yelp, events, weather) for suggestions

### Quest Completion Flow
1. User marks quest complete (honor system, no GPS needed)
2. System awards XP immediately
3. System logs quest category (social, constitutional, etc.)
4. System applies base mood buff ("quest completed +5")
5. System prompts: "Log additional mood modifiers?"
6. User optionally adds specific buffs/debuffs (pain, energized, etc.)

## Traits System

### Philosophy
- **Min traits:** 0 (optional system)
- **Max traits:** 5
- **Set during initial setup** but always editable via Settings
- **Affect quest suggestions** (v2 feature - bookmark for later)

### Examples
- RimWorld traits: "Optimist (+5)", "Pessimist (-5)", "Night Owl", etc.
- Future: Myers-Briggs as trait ("ENTP", "ISFJ") - affects quest matching

## Aesthetic & Feel

### Visual Inspiration
- **Legend of the Red Dragon** (BBS door game reference)
- **90s cyber / Hackers movie aesthetic**
- **Tribal hints** (nod to surrealist/situationist framework)
- **Lots of color** (ANSI colors, Rich library)
- **Feel over perfection** - Iterate to find what's right

### Boot Sequence
- **"Dialing in" simulation** (yes!)
- **MOTD (Message of the Day)** (yes!)
- **Last login display** (yes!)
- **ASCII art splash screen**

### UI Principles
- Box-drawing characters for borders
- Color-coded mood states (green/yellow/red)
- ASCII faces for mood (`:D`, `:)`, `:|`, `:(`, `D:`)
- Always-visible status bar with key info

## API & Integration (Future)

### Primary Use Cases
- **Home automation** - Lights adjust based on mood
- **Voice assistants** - "Hey Siri, what's my current mood?"
- **Other apps** - Automatic event logging

### Security Model
- **LAN-only** for now
- **No authentication required** (trust-based, single-user)
- **Read/write access** for trusted devices
- **Long-term plan:** TBD based on usage patterns

## Feature Roadmap

### MVP (v1) ✓
- Core mood tracking with RimWorld modifiers
- Quest system with manual entry
- Dashboard, WanderMOO, MoodStats, LogAction
- SQLite persistence
- Rich-based ASCII UI
- Numpad-friendly navigation

### v2 (Next Priority)
1. **Expedition Log** - Track places visited, create digital artifacts
2. **RimWorld-style memory system** - Generate memories from logged events
3. **Expanded boot sequence** - Dialing in, MOTD, last login
4. **Trait-based quest matching** - Quests match personality traits
5. **Recurring quest system** - Daily/weekly goals
6. **Enhanced mood modifier library** - More customizable events

### v3 (Future Ideas)
- Ongoing text narrative / evolving personal lore
- Location-aware quest refinement (learn user preferences)
- Mood-based quest suggestions (match quests to current state)
- API for home automation and voice assistant integration
- Quest generation from external APIs (Yelp, events, weather)

### Not Prioritized
- ~~Colony events / idle animations~~ (doesn't fit the model)
- GPS/location verification (honor system preferred)

## Success Metrics

How we'll know MOOdBBS is working:

1. **Daily usage** - User checks in multiple times per day
2. **Consistent logging** - Events logged within hours of occurrence
3. **Quest completion rate** - Quests inspire real-world action
4. **Mood pattern awareness** - User gains insights from historical data
5. **Sustained engagement** - System remains useful beyond novelty phase

## Design Constraints

1. **Keep it simple** - Resist feature creep in early versions
2. **Favor extensibility** - User should be able to customize without code changes
3. **Honor the aesthetic** - 90s BBS feel is essential, not cosmetic
4. **No judgment** - System never scolds or pressures
5. **Quick interactions** - Most actions under 10 seconds

## Open Questions

1. How to best auto-generate quests that feel personal and interesting?
2. What's the right balance of stock vs. custom mood modifiers?
3. How granular should quest categories be?
4. Should XP actually do anything, or is it purely cosmetic?
5. How to make the "memory system" feel meaningful vs. gimmicky?

These will be answered through usage and iteration.
