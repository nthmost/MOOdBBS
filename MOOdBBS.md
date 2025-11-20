Project:  MOOdBBS + WanderMOO
1. Purpose

A local, always-on ASCII dashboard running on a small monitor in your home, acting as a personal RimWorld-style mood tracker and MUD/MOO-style daily quest board.

It logs mood-relevant events with near-zero friction via a physical numpad, offering nested menus for quick logical input.

Also offers an API for remote querying of user's current state as well as allowing other local network devices to update user's current state.  (For now, just being on the LAN is our "security".

When the thing boots up, users see "MOOdBBS" with some hokey 90s ASCII art and then will be able to choose options as if picking door games. "WanderMOO" will be one of those "games": the method by which quests are received and reported on.

The goal:

Reflect your current “mood buffs/debuffs” back at you in a non-judgmental, game-like way.  (Why: because sometimes you know you feel kinda bad, but you forget all the little cuts and scrapes that got you to this point -- and when you realize this, you can be kinder to yourself.   Or if you feel really good, you can look at all the good self-care you've done, and reinforce your concept of how good moods really come to be.)

Suggest real-world quests and explorations (e.g. “Go to Coit Tower before 4pm”, "go get your nails done", "bike to the ocean", "take a jog to a cafe a little further away", "walk up a hill to see the sunset").

Track moods using an arbitrary point system reminiscent of Rimworld.  ("Ate without table: -3".  "Too long indoors: -whatever", etc) (MVP can just copy RImworld's mood system entirely and we can tweak from there.)

Integrate Rimworld Traits for user by having user select traits from a menu system.

100% ASCII based with a classic 90s BBS door game feel -- but bringing the power of modern information technology to bear, e.g. real-time weather display for user's zip code on Home Screen.

2. Core Components (MVP)
A. ASCII Dashboard (Kitchen Display)

Runs on any Linux box or Pi with a mini monitor.

Displays:

Mood Bar

Aggregated score based on logged modifiers

e.g. Indoors too long, Ate without table, Social interaction, Completed a walk

Shows RimWorld-style mood face (ASCII)

Active Quests

Up to 3 quests

Each with title + short description

Track XP reward on completion

Time display options:
* weekly counter w/ reset on Mondays (i.e. "completed x walks")
* N days ago (e.g. "you went for a walk 2 days ago")

Items considered salient to mood that have to do with quests:
* got outdoors
* visited a new place
* did a chore
* saw a friend
* interacted with strangers

Never destroy data: Keep activity and mood history.

System Time & Simple Status Line

e.g., “Weather: Clear. Sunset in 1h 12m.”

B. Input System (Numpad-Based)

We'll just use a standard keyboard at first, then transition to only needing to have a small USB numpad connected to the host device.

Top level menu (i.e. when MOOdBBS loads and the "dashboard" is displayed):

1. WanderMOO
2. MOOdBoard [log mood buffs and debuffs, see more detail about my mood]
3. [tbd - show history?]
4. [tbd - toggle dashboard modes?]





3. Likely MVP implementation

Rich based interface using python
Sqlite backed
Run on development machine, deployment TBD


4. Success Criteria for MVP

Numpad inputs instantly reflect on the ASCII dashboard.

Quest completion updates XP and reduces active quests list.

Quest completion asks user if they want to log mood -- if so, transition from WanderMOO to MOOdBoard

Mood score reacts appropriately to logged modifiers.

API should allow other processes to:

* Log events
* Add quests
* Discover current mood status

Whole system survives a reboot.

5. Future Adjacent Ideas (not in MVP)

Ongoing text narrative / evolving personal lore

Location-aware quests (GPS or neighborhood radius) that take current mood into account.

Idle animations or “colony events”

Mood-based environmental triggers (lights, soundscapes)

Dedicated “Expedition Log” for places visited

RimWorld-style memory system (“Had a fine meal,” “Saw art,” etc.)

