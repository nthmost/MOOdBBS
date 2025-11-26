-- MOOdBBS Database Schema

-- Quests table
CREATE TABLE IF NOT EXISTS quests (
    id INTEGER PRIMARY KEY,
    template_id TEXT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    location TEXT,
    xp_reward INTEGER NOT NULL,
    status TEXT NOT NULL,
    renewal_type TEXT,
    renewal_cooldown_days INTEGER,
    renewal_active_months TEXT,
    next_eligible_renewal TEXT,
    renewal_count INTEGER DEFAULT 0,
    constraint_type TEXT,
    constraint_note TEXT,
    created_at TEXT NOT NULL,
    completed_at TEXT,
    due_at TEXT
);

-- Quest completions table
CREATE TABLE IF NOT EXISTS quest_completions (
    id INTEGER PRIMARY KEY,
    quest_id INTEGER NOT NULL,
    completed_at TEXT NOT NULL,
    location_visited TEXT,
    duration_minutes INTEGER,
    notes TEXT,
    xp_awarded INTEGER NOT NULL,
    FOREIGN KEY (quest_id) REFERENCES quests (id)
);

-- Quest completion mood modifiers (many-to-many)
CREATE TABLE IF NOT EXISTS quest_completion_modifiers (
    completion_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    modifier INTEGER NOT NULL,
    FOREIGN KEY (completion_id) REFERENCES quest_completions (id)
);

-- Quest snoozes table
CREATE TABLE IF NOT EXISTS quest_snoozes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quest_id INTEGER NOT NULL,
    snoozed_at TEXT NOT NULL,
    reason_category TEXT,
    reason_text TEXT,
    context_data TEXT,
    FOREIGN KEY (quest_id) REFERENCES quests (id)
);

-- Mood events table
CREATE TABLE IF NOT EXISTS mood_events (
    id INTEGER PRIMARY KEY,
    event_type TEXT NOT NULL,
    modifier INTEGER NOT NULL,
    description TEXT,
    created_at TEXT NOT NULL,
    expires_at TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);

-- Traits table
CREATE TABLE IF NOT EXISTS traits (
    id INTEGER PRIMARY KEY,
    trait_name TEXT NOT NULL,
    description TEXT,
    mood_modifier INTEGER NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    category TEXT NOT NULL
);

-- User stats table (singleton)
CREATE TABLE IF NOT EXISTS user_stats (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    total_xp INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- User profile table (singleton)
CREATE TABLE IF NOT EXISTS user_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    home_neighborhood TEXT,
    home_address TEXT,
    home_zipcode TEXT,
    memberships TEXT,  -- JSON array
    has_car INTEGER DEFAULT 0,
    prefers_walking INTEGER DEFAULT 1,
    prefers_transit INTEGER DEFAULT 1,
    prefers_biking INTEGER DEFAULT 0,
    easy_distance REAL DEFAULT 0.5,
    medium_distance REAL DEFAULT 2.0,
    hard_distance REAL DEFAULT 5.0,
    setup_completed INTEGER DEFAULT 0,  -- First-run setup flag
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_quests_status ON quests(status);
CREATE INDEX IF NOT EXISTS idx_quests_created_at ON quests(created_at);
CREATE INDEX IF NOT EXISTS idx_quest_completions_quest_id ON quest_completions(quest_id);
CREATE INDEX IF NOT EXISTS idx_quest_completions_completed_at ON quest_completions(completed_at);
CREATE INDEX IF NOT EXISTS idx_mood_events_created_at ON mood_events(created_at);
CREATE INDEX IF NOT EXISTS idx_mood_events_is_active ON mood_events(is_active);
CREATE INDEX IF NOT EXISTS idx_traits_is_active ON traits(is_active);

-- Initialize user stats if doesn't exist
INSERT OR IGNORE INTO user_stats (id, total_xp, created_at, updated_at)
VALUES (1, 0, datetime('now'), datetime('now'));

-- Initialize user profile with defaults (setup not completed)
INSERT OR IGNORE INTO user_profile (
    id, home_neighborhood, memberships, has_car, prefers_walking, prefers_transit, prefers_biking, setup_completed,
    created_at, updated_at
) VALUES (
    1, NULL, '[]', 0, 1, 1, 0, 0,
    datetime('now'), datetime('now')
);
