-- Migration 007: Add negative social moodlets (and positive flirting)
-- Covers rejection, unwanted advances, and various levels of being dumped

INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    -- Positive flirting
    (103, 'Flirted (welcome)', 'social', 5, 4, NULL, NULL, 'Enjoyed mutual flirtation', 0),

    -- Negative flirting
    (104, 'Flirted (unwelcome)', 'social', -5, 2, NULL, NULL, 'Received unwanted advances', 0),

    -- Rejection with backoff
    (105, 'Rejected', 'social', -10, 24, -5, 12, 'Turned down (job, date, proposal, etc.)', 0),

    -- Different severities of being dumped (user should choose appropriate one)
    (106, 'Dumped (casual)', 'social', -8, 48, -4, 48, 'Casual relationship ended', 0),
    (107, 'Dumped (serious)', 'social', -15, 72, -8, 120, 'Significant relationship ended', 0),
    (108, 'Dumped (long-term)', 'social', -25, 168, -12, 336, 'Long-term relationship ended', 0),
    (109, 'Friend breakup', 'social', -12, 96, -6, 72, 'Lost a close friendship', 0);
