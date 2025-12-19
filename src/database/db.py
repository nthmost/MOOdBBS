"""Database connection and operations for MOOdBBS."""

import sqlite3
import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timezone
from contextlib import contextmanager

from src.domain.quests import Quest, QuestCompletion, RenewalPolicy, QuestSnooze
from src.domain.mood import MoodEvent
from src.domain.traits import Trait
from src.domain.user_profile import UserProfile


class Database:
    """SQLite database adapter for MOOdBBS."""

    def __init__(self, db_path: str = "data/moodbbs.db"):
        """Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path

        # Ensure data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        # Initialize schema
        self._init_schema()

    @contextmanager
    def _get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_schema(self):
        """Initialize database schema."""
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, 'r') as f:
            schema = f.read()

        with self._get_connection() as conn:
            conn.executescript(schema)

    # ==================== Quest Operations ====================

    def save_quest(self, quest: Quest):
        """Save or update a quest."""
        with self._get_connection() as conn:
            # Serialize renewal policy
            renewal_type = None
            renewal_cooldown_days = None
            renewal_active_months = None

            if quest.renewal_policy:
                renewal_type = quest.renewal_policy.renewal_type
                renewal_cooldown_days = quest.renewal_policy.cooldown_days
                if quest.renewal_policy.active_months:
                    renewal_active_months = json.dumps(quest.renewal_policy.active_months)

            conn.execute('''
                INSERT OR REPLACE INTO quests (
                    id, template_id, title, description, category, difficulty,
                    location, xp_reward, status, renewal_type, renewal_cooldown_days,
                    renewal_active_months, next_eligible_renewal, renewal_count,
                    constraint_type, constraint_note, created_at, completed_at, due_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                quest.id, quest.template_id, quest.title, quest.description,
                quest.category, quest.difficulty, quest.location, quest.xp_reward,
                quest.status, renewal_type, renewal_cooldown_days, renewal_active_months,
                quest.next_eligible_renewal.isoformat() if quest.next_eligible_renewal else None,
                quest.renewal_count, quest.constraint_type, quest.constraint_note,
                quest.created_at.isoformat(),
                quest.completed_at.isoformat() if quest.completed_at else None,
                quest.due_at.isoformat() if quest.due_at else None
            ))

    def load_quests(self) -> List[Quest]:
        """Load all quests from database."""
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM quests')
            rows = cursor.fetchall()

        quests = []
        for row in rows:
            # Deserialize renewal policy
            renewal_policy = None
            if row['renewal_type']:
                active_months = None
                if row['renewal_active_months']:
                    active_months = json.loads(row['renewal_active_months'])

                renewal_policy = RenewalPolicy(
                    renewal_type=row['renewal_type'],
                    cooldown_days=row['renewal_cooldown_days'],
                    active_months=active_months
                )

            quest = Quest(
                id=row['id'],
                template_id=row['template_id'],
                title=row['title'],
                description=row['description'],
                category=row['category'],
                difficulty=row['difficulty'],
                location=row['location'],
                xp_reward=row['xp_reward'],
                status=row['status'],
                renewal_policy=renewal_policy,
                next_eligible_renewal=datetime.fromisoformat(row['next_eligible_renewal']) if row['next_eligible_renewal'] else None,
                renewal_count=row['renewal_count'],
                created_at=datetime.fromisoformat(row['created_at']),
                completed_at=datetime.fromisoformat(row['completed_at']) if row['completed_at'] else None,
                due_at=datetime.fromisoformat(row['due_at']) if row['due_at'] else None,
                constraint_type=row['constraint_type'],
                constraint_note=row['constraint_note']
            )
            quests.append(quest)

        return quests

    def get_next_quest_id(self) -> int:
        """Get next available quest ID."""
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT MAX(id) as max_id FROM quests')
            row = cursor.fetchone()
            return (row['max_id'] or 0) + 1

    def save_quest_completion(self, completion: QuestCompletion):
        """Save a quest completion record."""
        with self._get_connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO quest_completions (
                    id, quest_id, completed_at, location_visited,
                    duration_minutes, notes, xp_awarded
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                completion.id, completion.quest_id,
                completion.completed_at.isoformat(),
                completion.location_visited, completion.duration_minutes,
                completion.notes, completion.xp_awarded
            ))

            # Save mood modifiers
            for event_type, modifier in completion.mood_modifiers_logged:
                conn.execute('''
                    INSERT INTO quest_completion_modifiers (
                        completion_id, event_type, modifier
                    ) VALUES (?, ?, ?)
                ''', (completion.id, event_type, modifier))

    def load_quest_completions(self) -> List[QuestCompletion]:
        """Load all quest completions from database."""
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM quest_completions')
            rows = cursor.fetchall()

        completions = []
        for row in rows:
            # Load mood modifiers for this completion
            cursor = conn.execute('''
                SELECT event_type, modifier
                FROM quest_completion_modifiers
                WHERE completion_id = ?
            ''', (row['id'],))
            modifiers = [(r['event_type'], r['modifier']) for r in cursor.fetchall()]

            completion = QuestCompletion(
                id=row['id'],
                quest_id=row['quest_id'],
                completed_at=datetime.fromisoformat(row['completed_at']),
                location_visited=row['location_visited'],
                duration_minutes=row['duration_minutes'],
                notes=row['notes'],
                mood_modifiers_logged=modifiers,
                xp_awarded=row['xp_awarded']
            )
            completions.append(completion)

        return completions

    def get_next_completion_id(self) -> int:
        """Get next available completion ID."""
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT MAX(id) as max_id FROM quest_completions')
            row = cursor.fetchone()
            return (row['max_id'] or 0) + 1

    # ==================== Mood Event Operations ====================

    def save_mood_event(self, event: MoodEvent):
        """Save or update a mood event."""
        with self._get_connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO mood_events (
                    id, event_type, modifier, description,
                    created_at, expires_at, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                event.id, event.event_type, event.modifier, event.description,
                event.created_at.isoformat(),
                event.expires_at.isoformat() if event.expires_at else None,
                1 if event.is_active else 0
            ))

    def load_mood_events(self) -> List[MoodEvent]:
        """Load all mood events from database."""
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM mood_events ORDER BY created_at DESC')
            rows = cursor.fetchall()

        events = []
        for row in rows:
            event = MoodEvent(
                id=row['id'],
                event_type=row['event_type'],
                modifier=row['modifier'],
                description=row['description'],
                created_at=datetime.fromisoformat(row['created_at']),
                expires_at=datetime.fromisoformat(row['expires_at']) if row['expires_at'] else None,
                is_active=bool(row['is_active'])
            )
            events.append(event)

        return events

    def get_next_mood_event_id(self) -> int:
        """Get next available mood event ID."""
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT MAX(id) as max_id FROM mood_events')
            row = cursor.fetchone()
            return (row['max_id'] or 0) + 1

    # ==================== Trait Operations ====================

    def save_trait(self, trait: Trait):
        """Save or update a trait."""
        with self._get_connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO traits (
                    id, trait_name, description, mood_modifier, is_active, category
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                trait.id, trait.trait_name, trait.description,
                trait.mood_modifier, 1 if trait.is_active else 0, trait.category
            ))

    def load_traits(self) -> List[Trait]:
        """Load all traits from database."""
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM traits')
            rows = cursor.fetchall()

        traits = []
        for row in rows:
            trait = Trait(
                id=row['id'],
                trait_name=row['trait_name'],
                description=row['description'],
                mood_modifier=row['mood_modifier'],
                is_active=bool(row['is_active']),
                category=row['category']
            )
            traits.append(trait)

        return traits

    def get_next_trait_id(self) -> int:
        """Get next available trait ID."""
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT MAX(id) as max_id FROM traits')
            row = cursor.fetchone()
            return (row['max_id'] or 0) + 1

    # ==================== User Stats Operations ====================

    def get_total_xp(self) -> int:
        """Get total user XP."""
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT total_xp FROM user_stats WHERE id = 1')
            row = cursor.fetchone()
            return row['total_xp'] if row else 0

    def set_total_xp(self, xp: int):
        """Set total user XP."""
        with self._get_connection() as conn:
            conn.execute('''
                UPDATE user_stats SET total_xp = ?, updated_at = datetime('now')
                WHERE id = 1
            ''', (xp,))

    # ==================== User Profile Operations ====================

    def get_user_profile(self) -> UserProfile:
        """Get user profile."""
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM user_profile WHERE id = 1')
            row = cursor.fetchone()

            if not row:
                # Return default profile if none exists
                from src.domain.user_profile import DEFAULT_PROFILE
                return DEFAULT_PROFILE

            memberships = json.loads(row['memberships']) if row['memberships'] else []

            # Helper to safely get column value with default
            def get_column(name, default=None):
                try:
                    return row[name]
                except (KeyError, IndexError):
                    return default

            return UserProfile(
                home_neighborhood=row['home_neighborhood'],
                home_address=row['home_address'],
                home_zipcode=get_column('home_zipcode'),
                memberships=memberships,
                has_car=bool(row['has_car']),
                prefers_walking=bool(row['prefers_walking']),
                prefers_transit=bool(row['prefers_transit']),
                prefers_biking=bool(get_column('prefers_biking', 0)),
                easy_distance=row['easy_distance'],
                medium_distance=row['medium_distance'],
                hard_distance=row['hard_distance'],
                setup_completed=bool(get_column('setup_completed', 0))
            )

    def save_user_profile(self, profile: UserProfile):
        """Save user profile."""
        with self._get_connection() as conn:
            memberships_json = json.dumps(profile.memberships)

            conn.execute('''
                INSERT OR REPLACE INTO user_profile (
                    id, home_neighborhood, home_address, home_zipcode, memberships,
                    has_car, prefers_walking, prefers_transit, prefers_biking,
                    easy_distance, medium_distance, hard_distance, setup_completed,
                    created_at, updated_at
                ) VALUES (
                    1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    COALESCE((SELECT created_at FROM user_profile WHERE id = 1), datetime('now')),
                    datetime('now')
                )
            ''', (
                profile.home_neighborhood, profile.home_address, profile.home_zipcode, memberships_json,
                1 if profile.has_car else 0,
                1 if profile.prefers_walking else 0,
                1 if profile.prefers_transit else 0,
                1 if profile.prefers_biking else 0,
                profile.easy_distance, profile.medium_distance, profile.hard_distance,
                1 if profile.setup_completed else 0
            ))

    # ==================== Moodlet Operations ====================

    def apply_moodlet(self, moodlet_id: int, source_quest_id: Optional[int] = None) -> int:
        """Apply a moodlet to the user.

        Args:
            moodlet_id: ID of the moodlet template to apply
            source_quest_id: Optional quest ID that triggered this moodlet

        Returns:
            ID of the new active moodlet instance
        """
        with self._get_connection() as conn:
            # Get moodlet template
            cursor = conn.execute('SELECT * FROM moodlets WHERE id = ?', (moodlet_id,))
            moodlet = cursor.fetchone()

            if not moodlet:
                raise ValueError(f"Moodlet {moodlet_id} not found")

            # Calculate expiration times
            from datetime import timedelta
            now = datetime.now(timezone.utc)
            expires_at = now + timedelta(hours=moodlet['duration_hours'])

            backoff_expires_at = None
            if moodlet['backoff_duration_hours']:
                backoff_expires_at = expires_at + timedelta(hours=moodlet['backoff_duration_hours'])

            # Insert active moodlet
            cursor = conn.execute('''
                INSERT INTO active_moodlets (
                    moodlet_id, applied_at, expires_at, backoff_expires_at,
                    is_in_backoff, source_quest_id
                ) VALUES (?, ?, ?, ?, 0, ?)
            ''', (
                moodlet_id,
                now.isoformat(),
                expires_at.isoformat(),
                backoff_expires_at.isoformat() if backoff_expires_at else None,
                source_quest_id
            ))

            return cursor.lastrowid

    def get_active_moodlets(self) -> List[Dict[str, Any]]:
        """Get all currently active moodlets with their template data."""
        with self._get_connection() as conn:
            now = datetime.now(timezone.utc).isoformat()

            cursor = conn.execute('''
                SELECT
                    am.id, am.applied_at, am.expires_at, am.backoff_expires_at,
                    am.is_in_backoff, am.source_quest_id,
                    m.name, m.category, m.mood_value, m.backoff_value, m.description
                FROM active_moodlets am
                JOIN moodlets m ON am.moodlet_id = m.id
                WHERE (am.is_in_backoff = 0 AND am.expires_at > ?)
                   OR (am.is_in_backoff = 1 AND am.backoff_expires_at > ?)
                ORDER BY am.applied_at DESC
            ''', (now, now))

            moodlets = []
            for row in cursor.fetchall():
                moodlets.append({
                    'id': row['id'],
                    'name': row['name'],
                    'category': row['category'],
                    'mood_value': row['backoff_value'] if row['is_in_backoff'] else row['mood_value'],
                    'description': row['description'],
                    'applied_at': row['applied_at'],
                    'expires_at': row['backoff_expires_at'] if row['is_in_backoff'] else row['expires_at'],
                    'is_in_backoff': bool(row['is_in_backoff']),
                    'source_quest_id': row['source_quest_id']
                })

            return moodlets

    def cleanup_expired_moodlets(self):
        """Remove expired moodlets and transition to backoff phase where applicable."""
        with self._get_connection() as conn:
            now = datetime.now(timezone.utc).isoformat()

            # Transition to backoff phase
            conn.execute('''
                UPDATE active_moodlets
                SET is_in_backoff = 1
                WHERE is_in_backoff = 0
                  AND expires_at <= ?
                  AND backoff_expires_at IS NOT NULL
                  AND backoff_expires_at > ?
            ''', (now, now))

            # Delete fully expired moodlets
            conn.execute('''
                DELETE FROM active_moodlets
                WHERE (is_in_backoff = 0 AND expires_at <= ?)
                   OR (is_in_backoff = 1 AND backoff_expires_at <= ?)
            ''', (now, now))

    def get_moodlets_by_category(self, category: str, is_quest_based: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get all moodlet templates in a category.

        Args:
            category: Category name (e.g., 'social', 'food', 'exercise')
            is_quest_based: Filter by quest-based (True) or event-based (False), or None for all

        Returns:
            List of moodlet template dictionaries
        """
        with self._get_connection() as conn:
            if is_quest_based is None:
                cursor = conn.execute('''
                    SELECT * FROM moodlets
                    WHERE category = ?
                    ORDER BY mood_value DESC
                ''', (category,))
            else:
                cursor = conn.execute('''
                    SELECT * FROM moodlets
                    WHERE category = ? AND is_quest_based = ?
                    ORDER BY mood_value DESC
                ''', (category, 1 if is_quest_based else 0))

            moodlets = []
            for row in cursor.fetchall():
                moodlets.append({
                    'id': row['id'],
                    'name': row['name'],
                    'category': row['category'],
                    'mood_value': row['mood_value'],
                    'duration_hours': row['duration_hours'],
                    'backoff_value': row['backoff_value'],
                    'backoff_duration_hours': row['backoff_duration_hours'],
                    'description': row['description'],
                    'is_quest_based': bool(row['is_quest_based'])
                })

            return moodlets

    def get_all_event_moodlets(self) -> List[Dict[str, Any]]:
        """Get all event-based (non-quest) moodlet templates, grouped by category."""
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM moodlets
                WHERE is_quest_based = 0 AND category != 'system'
                ORDER BY category, mood_value DESC
            ''')

            moodlets = []
            for row in cursor.fetchall():
                moodlets.append({
                    'id': row['id'],
                    'name': row['name'],
                    'category': row['category'],
                    'mood_value': row['mood_value'],
                    'duration_hours': row['duration_hours'],
                    'backoff_value': row['backoff_value'],
                    'backoff_duration_hours': row['backoff_duration_hours'],
                    'description': row['description'],
                    'is_quest_based': bool(row['is_quest_based'])
                })

            return moodlets
