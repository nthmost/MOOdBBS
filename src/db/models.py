"""Database models for MOOdBBS."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


class Database:
    """Main database interface for MOOdBBS."""

    def __init__(self, db_path: str = "data/moodbbs.db"):
        """Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.init_schema()

    def init_schema(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()

        # User traits table (RimWorld-style personality traits)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_traits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trait_name TEXT NOT NULL UNIQUE,
                description TEXT,
                mood_modifier INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Mood events table (tracks all mood-affecting events)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mood_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                modifier INTEGER NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)

        # Quests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                location TEXT,
                xp_reward INTEGER DEFAULT 10,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                due_at TIMESTAMP
            )
        """)

        # Quest completions (for tracking history)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quest_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quest_id INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                mood_logged BOOLEAN DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (quest_id) REFERENCES quests (id)
            )
        """)

        # Mood snapshots (periodic saves of aggregated mood state)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mood_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mood_score INTEGER NOT NULL,
                mood_face TEXT,
                active_modifiers TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Settings/config table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

    def add_mood_event(
        self,
        event_type: str,
        modifier: int,
        description: str = "",
        duration_hours: Optional[int] = None
    ) -> int:
        """Log a mood-affecting event.

        Args:
            event_type: Type of event (e.g., 'ate_without_table', 'social_interaction')
            modifier: Mood points to add/subtract
            description: Optional description
            duration_hours: How long this modifier lasts (None = permanent)

        Returns:
            ID of created event
        """
        cursor = self.conn.cursor()

        expires_at = None
        if duration_hours:
            from datetime import timedelta
            expires_at = datetime.now() + timedelta(hours=duration_hours)

        cursor.execute("""
            INSERT INTO mood_events (event_type, modifier, description, expires_at)
            VALUES (?, ?, ?, ?)
        """, (event_type, modifier, description, expires_at))

        self.conn.commit()
        return cursor.lastrowid

    def get_active_mood_events(self) -> List[Dict[str, Any]]:
        """Get all currently active mood events.

        Returns:
            List of active mood events as dicts
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM mood_events
            WHERE is_active = 1
            AND (expires_at IS NULL OR expires_at > datetime('now'))
            ORDER BY created_at DESC
        """)

        return [dict(row) for row in cursor.fetchall()]

    def calculate_current_mood(self) -> int:
        """Calculate current mood score from all active events and traits.

        Returns:
            Total mood score
        """
        events = self.get_active_mood_events()
        traits = self.get_active_traits()

        mood_score = 0

        # Add up event modifiers
        for event in events:
            mood_score += event['modifier']

        # Add trait modifiers
        for trait in traits:
            mood_score += trait['mood_modifier']

        return mood_score

    def add_quest(
        self,
        title: str,
        description: str = "",
        location: str = "",
        xp_reward: int = 10,
        due_hours: Optional[int] = None
    ) -> int:
        """Create a new quest.

        Args:
            title: Quest title
            description: Quest description
            location: Location/place for quest
            xp_reward: XP awarded on completion
            due_hours: Hours until quest expires (None = no deadline)

        Returns:
            ID of created quest
        """
        cursor = self.conn.cursor()

        due_at = None
        if due_hours:
            from datetime import timedelta
            due_at = datetime.now() + timedelta(hours=due_hours)

        cursor.execute("""
            INSERT INTO quests (title, description, location, xp_reward, due_at)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, location, xp_reward, due_at))

        self.conn.commit()
        return cursor.lastrowid

    def get_active_quests(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Get active quests.

        Args:
            limit: Maximum number of quests to return

        Returns:
            List of active quests as dicts
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM quests
            WHERE status = 'active'
            AND (due_at IS NULL OR due_at > datetime('now'))
            ORDER BY created_at ASC
            LIMIT ?
        """, (limit,))

        return [dict(row) for row in cursor.fetchall()]

    def complete_quest(self, quest_id: int, notes: str = "") -> bool:
        """Mark a quest as completed.

        Args:
            quest_id: ID of quest to complete
            notes: Optional completion notes

        Returns:
            True if quest was completed, False if not found
        """
        cursor = self.conn.cursor()

        # Update quest status
        cursor.execute("""
            UPDATE quests
            SET status = 'completed', completed_at = datetime('now')
            WHERE id = ? AND status = 'active'
        """, (quest_id,))

        if cursor.rowcount == 0:
            return False

        # Log completion
        cursor.execute("""
            INSERT INTO quest_completions (quest_id, notes)
            VALUES (?, ?)
        """, (quest_id, notes))

        self.conn.commit()
        return True

    def add_trait(self, trait_name: str, description: str = "", mood_modifier: int = 0) -> int:
        """Add a user trait (RimWorld-style).

        Args:
            trait_name: Name of trait
            description: Description of trait
            mood_modifier: Base mood modifier for this trait

        Returns:
            ID of created trait (or existing if duplicate)
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO user_traits (trait_name, description, mood_modifier)
                VALUES (?, ?, ?)
            """, (trait_name, description, mood_modifier))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Trait already exists
            cursor.execute("""
                SELECT id FROM user_traits WHERE trait_name = ?
            """, (trait_name,))
            return cursor.fetchone()[0]

    def get_active_traits(self) -> List[Dict[str, Any]]:
        """Get all active user traits.

        Returns:
            List of active traits as dicts
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM user_traits
            WHERE is_active = 1
            ORDER BY trait_name
        """)

        return [dict(row) for row in cursor.fetchall()]

    def save_mood_snapshot(self):
        """Save current mood state as a snapshot for history tracking."""
        mood_score = self.calculate_current_mood()
        events = self.get_active_mood_events()

        # Determine mood face based on score (RimWorld-style)
        if mood_score >= 20:
            mood_face = ":D"
        elif mood_score >= 10:
            mood_face = ":)"
        elif mood_score >= 0:
            mood_face = ":|"
        elif mood_score >= -10:
            mood_face = ":("
        else:
            mood_face = "D:"

        # Serialize active modifiers
        import json
        active_modifiers = json.dumps([
            {"type": e["event_type"], "modifier": e["modifier"]}
            for e in events
        ])

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO mood_snapshots (mood_score, mood_face, active_modifiers)
            VALUES (?, ?, ?)
        """, (mood_score, mood_face, active_modifiers))

        self.conn.commit()

    def close(self):
        """Close database connection."""
        self.conn.close()
