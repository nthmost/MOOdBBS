-- Migration 004: Add Self Care moodlets
-- Personal care activities with various durations and backoff effects

INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    -- Self-care moodlets with backoff (long-lasting effects)
    (80, 'Got a great haircut', 'selfcare', 10, 8, 4, 120, 'Fresh haircut feels amazing', 0),
    (81, 'Got my nails done', 'selfcare', 5, 4, 3, 120, 'Nails looking good', 0),
    (82, 'Did my skin care routine', 'selfcare', 5, 12, NULL, NULL, 'Skin feels refreshed and healthy', 0),

    -- Self-care moodlets without backoff (temporary relief)
    (83, 'Took a hot shower', 'selfcare', 3, 2, NULL, NULL, 'Clean and refreshed', 0),
    (84, 'Took a bath', 'selfcare', 5, 3, NULL, NULL, 'Relaxed and soothed', 0),
    (85, 'Watching comfort TV/movie', 'selfcare', 10, 1, NULL, NULL, 'Enjoying comfort media', 0);
