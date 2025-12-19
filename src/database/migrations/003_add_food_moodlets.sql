-- Migration 003: Add additional food moodlets
-- Adds "Ate a fine meal", "Ate a lavish meal", and "Whiskey warmth"

INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (70, 'Ate a fine meal', 'food', 6, 4, NULL, NULL, 'Had a really good meal', 0),
    (71, 'Ate a lavish meal', 'food', 9, 6, NULL, NULL, 'Enjoyed an exceptional feast', 0),
    (72, 'Whiskey warmth', 'food', 4, 1, NULL, NULL, 'The glow of good whiskey', 0);
