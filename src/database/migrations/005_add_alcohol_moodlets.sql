-- Migration 005: Add alcohol moodlets with negative backoff
-- Alcohol provides immediate boost but has a negative hangover effect later

INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    -- Alcohol moodlets with negative backoff (hangover effect)
    (90, 'Had a drink', 'food', 4, 2, -2, 12, 'Enjoyed an alcoholic beverage', 0),
    (91, 'Had a few drinks', 'food', 6, 3, -3, 12, 'Nice buzz going', 0),
    (92, 'Got tipsy', 'food', 8, 4, -4, 12, 'Feeling good and loose', 0);

-- Update existing whiskey warmth to have negative backoff
UPDATE moodlets
SET backoff_value = -2, backoff_duration_hours = 12
WHERE id = 72;
