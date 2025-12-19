**Quest XP Philosophy Part 2**


 Gaps & Questions I See:

  1. Relative Difficulty Problem (You mentioned this!)

  You said: "A medium difficulty thing for ME might be a bike ride that takes 30-45 minutes and involves 500 feet of elevation gain. That might be very 
  difficult for someone else, or too easy for some other person."

  Possible solutions:
  - Option A: User sets difficulty level during quest creation/acceptance
    - Quest: "Bike to Golden Gate Park"
    - User chooses: Easy (20 XP), Medium (35 XP), Hard (50 XP) based on their fitness
  - Option B: Quest tags with difficulty indicators
    - User profile stores fitness level, system suggests appropriate quests
  - Option C: Just accept variance
    - Everyone gets same XP, but some people find it easier - that's okay?


I guess I want to incorporate a bit of quest feedback when someone completes a quest.  "How hard did this feel today?"  With a ranking that matches our XP scaling system from micro to epic.

I think I do want to implement this in the current iteration because I think it will help me and others w/ ADHD and autism start to get a better feel for "what it actually takes to do the thing", which is something we can easily forget about, and then what we do is underestimate the effort and thus undervalue the rewards we might get from it.

To help with this tendency, I want to collect information that helps adjust the difficulty rankings of the quests. 

Bike rides should be assessed by the total length in miles, the elevation gain, and any weather that might impede motion (wind especially) on that particular day. (It would be cool to make the quest system SHOW that it has taken this into account by incorporating a statement about the weather, btw!  Perhaps a little wind emoji if it's a windier day followed by a "+3 for high wind today" explaining why the total XP for this quest is a little higher than it would be otherwise.)


  2. Starter Quest Problem

  You want specificity ("walk to Coit Tower at sunset") but also universality (works anywhere in world). These are in tension!

ARE THEY? This is why we are collecting info about a person's zip code and using an LLM to help generate quests!


  Possible resolution:
  - Universal starter pack: Generic but still somewhat specific
    - "Walk to nearest park" (system doesn't know which park yet)
    - "Visit a coffee shop you've never been to"
    - "Walk around your block 3 times"
  - Location-aware quests come AFTER setup (when we know zipcode)
    - Then we generate: "Walk to Alta Plaza Park before 4pm"


Yeah, we can use generic quests if the person doesn't want to input their location.  But I want to set up this system such that the person really WANTS to put their zip code in.

We should think about making sure people can set which specific locations are their favorites, btw.  I'm not sure we've denoted that anywhere yet.


  3. XP Scale Calibration

  If easy = 2-5 XP and hard = 45-100 XP, what's the middle?

  Proposed tiers:
  - Micro (1-3 XP): Log mood, drink water, stretch
  - Easy (4-8 XP): 15-min walk, say hi to stranger
  - Medium (10-20 XP): Visit new place, meaningful conversation
  - Hard (25-45 XP): Big adventure, fitness challenge
  - Epic (50-100 XP): Bucket list item, major achievement

  Sound right?

This is totally feelings-based but I think 25XP should be the upper limit on Medium.  Hard then starts at 26 and tops out at 50XP.   Epic is fine as is.

Btw as a math major your discontinuous number line disturbs me. :D 

Micro 1-3 is fine, Easy would then be 4 to 9.


  4. Moodlet Triggers

  You listed 4 exercise moodlets. When does each trigger?

  My guess:
  - Refreshed (+3): Short walk (15-20 min)
  - Energized (+5): Moderate exercise (30 min)
  - Pumped (+8): Intense workout (45+ min or high effort)
  - Physically Spent (+10, but -2 energy?): Exhausting effort


Speaking from personal experience with these states of being here's how I'd rewrite them:

* Refreshed and Energized make sense as-is, moodlets should last 2 hours and 4 hours respectively.  (No "backoff".)
* Pumped should be a +10 and should last 10 hours with a moodlet "backoff" to +5 that last another 4 hours which says "Workout glow"
* Physically Spent should be a huge buff at +15 and last 12 hours, followed by a moodlet "backoff" to +8 after 12 hours that then says "Hard Workout Glow"

  Do these need intensity or duration parameters? Or is it quest-specific?


Refer to the rimworld moodlet system for guidance here.
Ask me to clarify if you need.


  5. Streak Mechanics

  You want streaks shown visually. Details to figure out:

  - What counts toward a streak?
    - Logging in daily?  YES
    - Completing ANY quest daily?  SURE
    - Completing specific categories (e.g., exercise streak)?  YES, any TYPE of quest (not repeating specific quests).
  - Where shown? Dashboard? Main menu?  WHEREVER IT LOOKS GOOD -- I like the idea of expanding the main menu so that it has a personalized section
  - Visual style? "🔥 3 day streak" or more BBS-style?  LET'S PLAY WITH DIFFERENT IDEAS, NOT SURE YET
  - Streak breaks? Does missing one day reset to 0?   

For now, missing 1 day resets it to 0.  Let's bookmark the idea of "planned breaks" as a later feature.



  6. First-Time User Flow

  Current: Setup Wizard → Main Menu → Empty quest list

  Better flow:
  1. Setup Wizard
  2. "First login" mood event (+5) ✅
  3. Seed universal starter quests (5-10 generic ones)
  4. Show dashboard with quests ready to go
  5. User can immediately take action

  7. Quest Renewal/Expiration

  You mentioned quests need specificity like "watch sunset at 6pm". What happens after 6pm?

  - Auto-expire? Quest disappears
  - Auto-renew? "Watch sunset at 6pm tomorrow"
  - Manual snooze? User decides

We haven't yet talked about when the system generates new quests.  I think the system should generate a new set of quests every morning at 5am.  Whatever wasn't done can just fall away into the void, it's OK.

Quests that are meant to renew should renew at the right times.  Quests that were one-time-only (specific dates of events) will go away.  



  What I'd Like to Clarify:

  1. Relative difficulty: How do we handle it for MVP? Fixed XP and accept variance, or add difficulty selection?

Let's start with fixed XP for now and feel it out.


  2. Starter quests: Should they be intentionally less specific for universal appeal, then location-aware quests come later?

I don't see a reason to avoid location-aware quests at the beginning.  This is why we are incorporating an LLM: to make this MUCH easier.


  3. XP tiers: Does my 5-tier system (1-3, 4-8, 10-20, 25-45, 50-100) feel right? 
  4. Moodlet triggers: How do we decide which exercise gives which moodlet? Duration? Intensity? User input?

I think we will need the user to report back after quests in order to get this right.

E.g. we can USUALLY expect that after a strength workout the user feels "pumped" -- but if the workout was actually too easy they might not!  And they will need some way of getting that input back into the system so that the system can adjust and recommend a better workout that will actually cause "pumped" the next time.

Epic workouts are always going to be something like, "Hike up Mt. Errigal" (omg, that was epic! I did that in September) or "bike the Ossagon trail" (did that in July, that was truly exhausting and wonderful).  There won't be much ambiguity there, but we should still ask the user how they feel afterwards.


  5. Streaks: What counts as "maintaining a streak" and where should it display?

As talked about above.


----

FOLLOWUP:

  Quest Completion Feedback Flow

  When user completes a quest, we ask:

MAKE SURE THIS QUESTIONNAIRE IS OPTIONAL / SKIPPABLE -- and if user skips, just assign the default amount amount XP and the usual moodlet for this type of quest.

  1. Difficulty Assessment

  ┌─────────────────────────────────────────────┐
  │ Quest Completed: Walk to Alta Plaza Park    │
  ├─────────────────────────────────────────────┤
  │ How hard did this feel today?               │
  │                                             │
  │ [1] Micro    (easier than expected)        │
  │ [2] Easy     (about right)                 │
  │ [3] Medium   (challenging)                 │
  │ [4] Hard     (very challenging)            │
  │ [5] Epic     (exhausting!)                 │
  └─────────────────────────────────────────────┘

  2. Location Favoriting (if quest involves a location)

  ┌─────────────────────────────────────────────┐
  │ Would you like to return to Alta Plaza Park?│
  │                                             │
  │ [y] Yes    [n] No                           │
  └─────────────────────────────────────────────┘

  3. Return Frequency (if yes to #2)

  ┌─────────────────────────────────────────────┐
  │ How soon would you like to return?          │
  │                                             │
  │ [1] Tomorrow                                │
  │ [2] This week                               │
  │ [3] This month                              │
  │ [4] Sometime (no schedule)                  │
  └─────────────────────────────────────────────┘

CHANGE "This week" to "In a week"

ADD "In about 2 weeks"

CHANGE "This month" to "In about a month"


  4. Mood Impact (optional, for specific quest types)

  ┌─────────────────────────────────────────────┐
  │ How do you feel after this quest?           │
  │                                             │
  │ [1] Refreshed      (+3, 2 hours)           │
  │ [2] Energized      (+5, 4 hours)           │
  │ [3] Pumped         (+10, 10 hours)         │
  │ [4] Physically Spent (+15, 12 hours)       │
  │ [5] Skip                                    │
  └─────────────────────────────────────────────┘


  Quest Generation Impact:

  When generating new quests:
  - Check favorite locations
  - If location has return_frequency = 'daily' and last_visited < today, generate quest for that location
  - Prioritize favorites when building daily quest list

  UX Flow:

  User completes "Walk to Alta Plaza Park"
    ↓
  System shows: "Quest Completed! +12 XP"
    ↓
  Ask: "How hard did this feel?" → stores feedback, adjusts future XP
    ↓
  Ask: "Would you like to return to Alta Plaza Park?"
    ↓ (if yes)
  Ask: "How soon would you like to return?" → stores favorite location
    ↓
  (if exercise quest) Ask: "How do you feel?" → applies moodlet
    ↓
  Return to dashboard

  Questions:

  1. Location extraction: How do we identify if a quest has a location?
    - Parse quest title/description for location names?
    - Add location_name field when generating quests via LLM?

We should add a location_name field for storing quest information.  We probably also want to add a location_address field, otherwise we're going to be re-looking-up that information when we're calculating the distance away from the user's home.

For that matter, we should probably considering asking the user for their full address.  We should keep that optional, but encourage it so the system can calculate accurate distances.

At minimum, though, we will need the user's city or zip code to use this system in a way that's not just "take a walk to the park" (super generic).


  2. Return frequency logic:
    - "Tomorrow" = generate quest for this location every day -- YES
    - "In a week or so" = generate quest for this location on a single day next week
    - "In about a month" = generate at most once per month
    - "Sometime" = add to rotation but no schedule - YES

  3. Moodlet question: Should we only ask "How do you feel?" for exercise/outdoor quests? Or all quests?

We should have custom "how do you feel?" menus for each category.  So, exercise is all done.  Social and other categories would have different questionnaires.



