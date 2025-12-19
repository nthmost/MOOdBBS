-- Migration 002: Seed Moodlet Templates
-- Pre-populates the moodlets table with all defined moodlets

-- Exercise/Physical Activity Moodlets
INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (1, 'Refreshed', 'exercise', 3, 2, NULL, NULL, 'Got outside for a bit', 1),
    (2, 'Energized', 'exercise', 5, 4, NULL, NULL, 'Light workout put pep in my step', 1),
    (3, 'Pumped', 'exercise', 10, 10, 5, 4, 'Muscles feel swole, bruh', 1),
    (4, 'Physically Spent', 'exercise', 15, 12, 8, 12, 'Used everything I had!', 1);

-- Social Interaction Moodlets (Quest-based)
INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (10, 'Acknowledged', 'social', 2, 2, NULL, NULL, 'Complimented a stranger', 1),
    (11, 'Connected', 'social', 5, 4, NULL, NULL, 'Had a nice chat', 1),
    (12, 'Bonded', 'social', 8, 8, NULL, NULL, 'Meaningful conversation', 1),
    (13, 'Loved', 'social', 12, 12, 6, 12, 'Deep connection with friend/family', 1);

-- Social Interaction Moodlets (Event-based)
INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (14, 'Complimented', 'social', 4, 5, NULL, NULL, 'Someone complimented me', 0),
    (15, 'Fun Encounter', 'social', 6, 6, NULL, NULL, 'Had unexpected fun encounter', 0),
    (16, 'Hugged', 'social', 5, 3, NULL, NULL, 'Got a hug', 0),
    (17, 'Remembered', 'social', 3, 2, NULL, NULL, 'Someone remembered my name', 0),
    (18, 'Invited', 'social', 7, 8, NULL, NULL, 'Invited to something', 0);

-- Creative/Learning Moodlets (Quest-based)
INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (20, 'Engaged', 'creative', 3, 3, NULL, NULL, 'Tried something new', 1),
    (21, 'Accomplished', 'creative', 6, 6, NULL, NULL, 'Made progress on a project', 1),
    (22, 'Proud', 'creative', 9, 10, NULL, NULL, 'Created something meaningful', 1),
    (23, 'Brilliant', 'creative', 12, 12, 6, 8, 'Had a breakthrough!', 1);

-- Creative/Learning Moodlets (Event-based)
INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (24, 'Learned', 'creative', 4, 4, NULL, NULL, 'Learned something interesting', 0),
    (25, 'Problem Solved', 'creative', 6, 6, NULL, NULL, 'Solved a tricky problem', 0),
    (26, 'Work Praised', 'creative', 8, 8, NULL, NULL, 'Someone praised my work', 0),
    (27, 'Project Finished', 'creative', 10, 12, NULL, NULL, 'Finished a project', 0);

-- Exploration/Discovery Moodlets
INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (30, 'Curious', 'exploration', 3, 3, NULL, NULL, 'Explored somewhere nearby', 1),
    (31, 'Adventurous', 'exploration', 6, 6, NULL, NULL, 'Discovered a new place', 1),
    (32, 'Amazed', 'exploration', 9, 8, NULL, NULL, 'Found something unexpected', 1),
    (33, 'Wonder-struck', 'exploration', 12, 10, 6, 6, 'Saw something breathtaking', 1);

-- Food/Culinary Moodlets (Quest-based)
INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (40, 'Satisfied', 'food', 3, 2, NULL, NULL, 'Ate a decent meal', 1),
    (41, 'Delighted', 'food', 5, 4, NULL, NULL, 'Had something tasty', 1),
    (42, 'Luxuriated', 'food', 8, 6, NULL, NULL, 'Enjoyed a fine meal', 1),
    (43, 'Blissful', 'food', 10, 8, 5, 4, 'Ate something amazing', 1);

-- Food/Culinary Moodlets (Event-based, negatives)
INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (44, 'Ate without table', 'food', -3, 2, NULL, NULL, 'Ate without table', 0),
    (45, 'Ate nutrient paste', 'food', -5, 3, NULL, NULL, 'Ate nutrient paste', 0),
    (46, 'Skipped a meal', 'food', -4, 4, NULL, NULL, 'Skipped a meal', 0);

-- Rest/Relaxation Moodlets
INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (50, 'Calmer', 'rest', 3, 3, NULL, NULL, 'Took a break', 1),
    (51, 'Recharged', 'rest', 5, 5, NULL, NULL, 'Rested properly', 1),
    (52, 'Restored', 'rest', 8, 8, NULL, NULL, 'Got good sleep', 1),
    (53, 'Renewed', 'rest', 10, 12, 5, 6, 'Deeply rested', 1);

-- Culture/Art Moodlets
INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (60, 'Inspired', 'culture', 4, 4, NULL, NULL, 'Saw something artistic', 1),
    (61, 'Moved', 'culture', 6, 6, NULL, NULL, 'Experienced beautiful art', 1),
    (62, 'Transported', 'culture', 9, 8, NULL, NULL, 'Lost in a performance/exhibit', 1),
    (63, 'Transcendent', 'culture', 12, 10, 6, 8, 'Art changed my perspective', 1);

-- Special moodlet: First Login
INSERT INTO moodlets (id, name, category, mood_value, duration_hours, backoff_value, backoff_duration_hours, description, is_quest_based)
VALUES
    (100, 'Joined MOOdBBS!', 'system', 5, 24, NULL, NULL, 'Logged into MOOdBBS for the first time', 0);
