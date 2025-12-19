"""Database migration system for MOOdBBS."""

import sqlite3
from pathlib import Path
from typing import List


class MigrationRunner:
    """Handles database migrations."""

    def __init__(self, db_path: str = "data/moodbbs.db"):
        """Initialize migration runner.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.migrations_dir = Path(__file__).parent / "migrations"

    def _get_applied_migrations(self, conn: sqlite3.Connection) -> List[str]:
        """Get list of already applied migrations."""
        # Create migrations table if it doesn't exist
        conn.execute('''
            CREATE TABLE IF NOT EXISTS schema_migrations (
                migration_name TEXT PRIMARY KEY,
                applied_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        ''')
        conn.commit()

        cursor = conn.execute('SELECT migration_name FROM schema_migrations ORDER BY migration_name')
        return [row[0] for row in cursor.fetchall()]

    def _get_pending_migrations(self) -> List[Path]:
        """Get list of migration files that haven't been applied yet."""
        if not self.migrations_dir.exists():
            return []

        all_migrations = sorted(self.migrations_dir.glob('*.sql'))

        conn = sqlite3.connect(self.db_path)
        try:
            applied = set(self._get_applied_migrations(conn))
        finally:
            conn.close()

        return [m for m in all_migrations if m.name not in applied]

    def run_migrations(self) -> int:
        """Run all pending migrations.

        Returns:
            Number of migrations applied
        """
        pending = self._get_pending_migrations()

        if not pending:
            print("No pending migrations.")
            return 0

        conn = sqlite3.connect(self.db_path)
        count = 0

        try:
            for migration_file in pending:
                print(f"Applying migration: {migration_file.name}")

                with open(migration_file, 'r') as f:
                    migration_sql = f.read()

                # Execute migration
                conn.executescript(migration_sql)

                # Record migration as applied
                conn.execute(
                    'INSERT INTO schema_migrations (migration_name) VALUES (?)',
                    (migration_file.name,)
                )
                conn.commit()
                count += 1

                print(f"  ✓ Applied {migration_file.name}")

        except Exception as e:
            conn.rollback()
            print(f"  ✗ Migration failed: {e}")
            raise

        finally:
            conn.close()

        return count


def main():
    """Run migrations from command line."""
    runner = MigrationRunner()
    count = runner.run_migrations()
    print(f"\nApplied {count} migration(s).")


if __name__ == '__main__':
    main()
