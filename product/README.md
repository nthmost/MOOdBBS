# MOOdBBS Product Documentation

This directory contains product specifications, user research, and design documentation for MOOdBBS.

## Core Documents

### [PRODUCT_VISION.md](PRODUCT_VISION.md)
The foundational product vision document covering:
- Core philosophy and "real world as ARG" concept
- Target users and use cases
- RimWorld connection and mood tracking approach
- Quest system design
- Traits system
- Aesthetic principles (90s BBS, Hackers movie, tribal hints)
- Feature roadmap (v1, v2, v3)
- Success metrics
- Open questions

### [USER_PERSONAS.md](USER_PERSONAS.md)
Detailed user personas including:
- **The Wanderer** (primary persona - you, the creator)
- **The Self-Quantifier** (data-driven mood tracker)
- **The Retro Enthusiast** (BBS aesthetic lover)
- Anti-personas (who this is NOT for)
- User journey maps
- Retention strategies

### [TECHNICAL_REQUIREMENTS.md](TECHNICAL_REQUIREMENTS.md)
Comprehensive technical specifications:
- Display requirements (tiny/small/medium/large modes)
- Input requirements (keyboard → numpad transition)
- Data persistence and database schema
- Performance requirements
- Platform requirements (macOS, Pi, Linux)
- API requirements (future v3)
- UI framework (Rich library)
- Quest system data models
- Mood modifier specifications
- Boot sequence design
- Configuration management
- Testing requirements
- Deployment strategy

### [questionnaire_responses.txt](questionnaire_responses.txt)
Raw interview responses from the product manager/user #1 covering all aspects of the product vision.

## Mockups & Specs

### [mockups/v1/](mockups/v1/)
Original mockups and specifications that informed the MVP:
- **MOOdBBS.md** - Original project specification
- **MOOdBBS_mainmenu_mockup.md** - Main menu ASCII mockup
- **MOOdBBS_cnxn_screen_mockup.md** - Connection/boot screen
- **MOOdBBS_Settings_mockup.md** - Settings screen concept
- **MOOdBBS_About_mockup.md** - About screen
- **MOOdStats_mockup.md** - MoodStats screen
- **MOOdBBS_BuildRecs_from_ChatGPT.md** - Initial build recommendations

## Document History

### v1 Documentation (Current)
Created based on:
1. Original mockups and specifications
2. Product manager interview (questionnaire_responses.txt)
3. MVP implementation learnings

Documents the initial vision and MVP implementation.

### Future Versions
As MOOdBBS evolves, new versioned documentation will be added:
- `v2/` - Expedition Log and Memory System features
- `v3/` - API and advanced quest generation

## How to Use This Documentation

### For Development
1. Start with **PRODUCT_VISION.md** to understand the "why"
2. Review **USER_PERSONAS.md** to understand the "who"
3. Reference **TECHNICAL_REQUIREMENTS.md** for the "how"
4. Check **mockups/v1/** for original design intent

### For Product Planning
1. Review **PRODUCT_VISION.md** for feature roadmap
2. Check "Open Questions" section for unresolved decisions
3. Use **USER_PERSONAS.md** to evaluate new features
4. Update documentation as decisions are made

### For Onboarding
1. Read **PRODUCT_VISION.md** first
2. Skim **USER_PERSONAS.md** to understand use cases
3. Review **mockups/v1/MOOdBBS.md** for original concept
4. Refer to **TECHNICAL_REQUIREMENTS.md** as needed

## Key Principles

These principles guide all product decisions:

1. **Non-judgmental reflection** - Show data, don't scold
2. **Near-zero friction** - Most interactions under 10 seconds
3. **Honor the aesthetic** - 90s BBS feel is essential
4. **User extensibility** - User should be able to customize
5. **Real world as ARG** - Turn daily life into gameplay

## Design Philosophy

### The RimWorld Connection
MOOdBBS uses RimWorld's mood system as a mental model:
- Simple integer-based modifiers
- Recognizable mood buffs and debuffs
- Arbitrary but relatable thresholds
- Stock modifiers + user customization

### The BBS Aesthetic
90s bulletin board system aesthetic with modern power:
- ANSI colors and ASCII art
- Box-drawing characters
- Boot sequences and MOTD
- Legend of the Red Dragon inspiration
- Hackers movie cyber aesthetic with tribal hints

### The Quest Philosophy
Quests provide **optionality** not **rigidity**:
- "Walk to a bookstore" (flexible) not "Walk to City Lights at 3pm" (rigid)
- Honor system completion (no GPS tracking)
- Recyclable quests (no penalty for skipping)
- Categories: social, constitutional, creative, experiential

## Version Roadmap

### v1 - MVP (Complete)
Core mood tracking, basic quests, ASCII UI, persistence

### v2 - Depth (Next)
Expedition Log, Memory System, recurring quests, enhanced boot sequence

### v3 - Integration (Future)
API, home automation, voice assistants, quest generation from external sources

## Contributing to Documentation

When updating product docs:
1. Keep **PRODUCT_VISION.md** as the source of truth
2. Update **USER_PERSONAS.md** when user insights emerge
3. Update **TECHNICAL_REQUIREMENTS.md** when technical decisions are made
4. Version mockups when designs change significantly
5. Document decisions in relevant files

## Questions or Feedback

For questions about product direction, refer to:
- Open Questions section in PRODUCT_VISION.md
- Anti-personas in USER_PERSONAS.md (what NOT to build)
- Future Considerations in TECHNICAL_REQUIREMENTS.md

---

**Last Updated:** 2025-11-20 (v1 documentation complete)
