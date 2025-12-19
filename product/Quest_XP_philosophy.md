 XP System Philosophy

  What should XP represent?
  - Effort (how hard was it?)
  - Time investment (how long did it take?)
  - Friction overcome (did you have to leave your comfort zone?)
  - Value to wellbeing (does this meaningfully improve mood/health?)


XP should represent a reasonable combo of effort, time, and friction.

XP should NOT represent the value to mood/health.  This is a separate metric with its own point system, which I think is important to keep distinct.

---

  Accessibility & Personalization Issues

  You're right about the pushups example - this raises important questions:

  1. Physical capability variance: What's easy for one person is impossible for another
  2. Context dependency: "Visit a café" assumes you can afford it, have transportation, etc.
  3. Personal goals: Someone training for a marathon vs. someone starting from sedentary

  Possible Solutions

  Option A: Baseline XP for Intent

  - Award XP for attempting fitness goals regardless of quantity
  - "Did physical exercise" = 5 XP (whether it's 1 pushup or 100)
  - Focus on the habit not the achievement

  Option B: User-Calibrated Goals

  - During setup, ask about fitness level
  - Generate personalized fitness quests (e.g., "Do 5 pushups" vs "Do 50 pushups")
  - Same XP, different difficulty based on user

  Option C: Progressive Goal System

  - Quests can have user-adjustable targets
  - "I completed [X] pushups" - user fills in the number
  - XP scales with personal improvement over time (beat your own record = bonus XP)

  Option D: Category-Based XP Tiers

  Micro-actions (1-3 XP): Near-zero friction
  - Drink water: 2 XP
  - Stand up and stretch: 2 XP
  - Log your mood: 1 XP

  Easy actions (4-8 XP): Low effort, anyone can do
  - 15-minute walk: 6 XP
  - Say hi to someone: 5 XP
  - Look at something beautiful for 1 min: 4 XP

  Medium effort (10-20 XP): Requires intention/planning
  - Visit somewhere new: 15 XP
  - Try new food: 12 XP
  - Have meaningful conversation: 15 XP
  - Physical exercise (self-defined): 10 XP

  High effort (25-50 XP): Significant time/energy
  - Go somewhere on bucket list: 30 XP
  - Complete multiple quests in one day: 25 XP
  - Attend an event: 40 XP

  Fitness Goals Integration

  Great idea about using this for fitness tracking! We could:

  1. Fitness Quest Templates with user-defined targets:
    - "Walk [distance]"
    - "Exercise for [minutes]"
    - "Do [activity]"

These are awful templates for reasons I go into later. 


  2. Progress Tracking: Store personal records in user profile
    - "Walked 5km (new record!)" = bonus XP

We should definitely consider "personal records", but this is getting outside the scope of the first iteration -- bookmark this for a later feature.


  3. Streak Bonuses: Exercise 3 days in a row = extra XP

I do love "streaks".  Let's add that in right away -- I want to see a visual indicator of a streak on the menu somewhere.


  4. Fitness Traits: "Physically active" vs "Building fitness" could affect mood differently

Yeah, these "moodlets" as Rimworld calls them could be along the lines of (long description in brackets):

* Refreshed ["I'm glad I got outside for a little bit."]
* Energized ["A light workout recently put some pep in my step"]
* Pumped ["That workout made my muscles feel extra swole, bruh"]
* Physically Spent ["I used everything I had! I feel amazing but tired."]
* ...

We can come up with more, feel free to suggest, but those cover a lot of bases.


  Questions for You:

  1. Should XP be effort-based (harder = more XP) or value-based (better for wellbeing = more XP)?

The point of the system is to demonstrate to the user that there's value both in doing small/easy things and in doing harder things.  Many people with ADHD or autism have an all-or-nothing bias that clouds reasoning and prevents us from doing easy things that actually may have a strong impact on our mood.

XP is an external way of motivating these small actions.  And showing 3 possible quests is a way of constraining the space of small possibilities.  Finally, since this system is tracking what we do, there's a value in being able to see the history of what we did and how it impacted our mood over time.


  2. Do you want fixed XP per quest or dynamic XP based on personal progress?

I think "pushups" should always have the same XP value.  The only thing that will change is the difficulty of that set (15 pushups is harder than 10, even though the amount of time it takes isn't significantly more).  This is consistent with the theory of progressive overload that helps just about every human on earth become stronger.

We can consider also the difference between "walking" and "hiking".  A "walk" should be expected to produce a feeling of being "energized"


  3. Should there be diminishing returns (e.g., 1st walk today = 6 XP, 2nd walk = 3 XP)?

No way, this would undermine the virtue of the system in making sure people understand that doing several small things has plenty of value.  What we want to watch out for is scaling XP so we don't get weird math like "3 short walks equals one medium bike ride."  This is why I'd like to make easy things quite low in XP (5XP max, 3XP avg), and hard things rather high in XP (like 45 to 100).

A medium difficulty thing for ME might be a bike ride that takes 30-45 minutes and involves 500 feet of elevation gain.  That might be something very difficult for someone else, or too easy for some other person.  Relative difficulty is what we have to feel out here -- I'm not exactly sure how to do it but I don't think it'll be that complicated.  We should talk it out.


  4. What's more important: encouraging easy wins or rewarding challenging achievements?

They're equally important!   The most important thing is motivating the user to do SOMETHING.  The enemy is inaction.


  5. Should fitness quests be generic ("exercise") or specific ("walk 2km")?

Fitness should always be specific, even more specific than "walk 2km".  this is why we're concerned with where the user lives (zip code) -- we want to make REALLY specific recommendations such as "walk to the top of Some Hill Over There and watch the sunset at 6pm."

People with Autism and ADHD (like me!) are way more likely to take action on quests with specificity.  Without that, we end up staring at a quest thinking "I should do that" and failing to follow through, generating guilt and shame and avoidance.
