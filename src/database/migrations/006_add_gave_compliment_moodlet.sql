-- Migration 006: Add "Gave someone a compliment" social moodlet
-- Event-based version matching the quest-based "Acknowledged" moodlet

INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (95, 'Gave someone a compliment', 'social', 2, 2, NULL, NULL, 'Made someone feel good', 0);
