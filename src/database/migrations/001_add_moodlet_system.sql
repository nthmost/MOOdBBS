-- Migration 001: Add Moodlet System
-- Adds moodlets, active_moodlets, favorite_locations tables
-- Adds location and feedback fields to existing tables

-- Moodlets table (pre-populated templates)
CREATE TABLE IF NOT EXISTS moodlets (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,  -- 'exercise', 'social', 'creative', 'exploration', 'food', 'rest', 'culture'
    mood_value INTEGER NOT NULL,
    duration_hours INTEGER NOT NULL,
    backoff_value INTEGER,  -- NULL if no backoff
    backoff_duration_hours INTEGER,  -- NULL if no backoff
    description TEXT,
    is_quest_based INTEGER DEFAULT 1  -- 1 for quest-based, 0 for event-based
);

-- Active moodlets (instances currently affecting mood)
CREATE TABLE IF NOT EXISTS active_moodlets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 1,
    moodlet_id INTEGER NOT NULL,
    applied_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    backoff_expires_at TEXT,  -- NULL if no backoff or not in backoff yet
    is_in_backoff INTEGER DEFAULT 0,
    source_quest_id INTEGER,  -- NULL if event-based
    source_event_id INTEGER,  -- NULL if quest-based
    FOREIGN KEY (moodlet_id) REFERENCES moodlets(id)
);

-- Favorite locations (user's preferred places to revisit)
CREATE TABLE IF NOT EXISTS favorite_locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_name TEXT NOT NULL,
    location_address TEXT,
    return_frequency TEXT,  -- 'daily', 'weekly', 'biweekly', 'monthly', 'sometime'
    next_scheduled_date TEXT,  -- ISO date for next quest generation
    added_at TEXT DEFAULT (datetime('now')),
    last_visited TEXT,
    visit_count INTEGER DEFAULT 1
);

-- Add location fields to quests table
ALTER TABLE quests ADD COLUMN location_name TEXT;
ALTER TABLE quests ADD COLUMN location_address TEXT;

-- Add feedback fields to quest_completions table
ALTER TABLE quest_completions ADD COLUMN difficulty_feedback INTEGER;  -- 1-5 (Micro-Epic)
ALTER TABLE quest_completions ADD COLUMN moodlet_selected TEXT;  -- 'refreshed', 'energized', etc.

-- Add optional full address to user_profile
ALTER TABLE user_profile ADD COLUMN full_address TEXT;
ALTER TABLE user_profile ADD COLUMN latitude REAL;
ALTER TABLE user_profile ADD COLUMN longitude REAL;

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_active_moodlets_expires_at ON active_moodlets(expires_at);
CREATE INDEX IF NOT EXISTS idx_active_moodlets_user_id ON active_moodlets(user_id);
CREATE INDEX IF NOT EXISTS idx_favorite_locations_return_frequency ON favorite_locations(return_frequency);
CREATE INDEX IF NOT EXISTS idx_favorite_locations_next_scheduled ON favorite_locations(next_scheduled_date);
