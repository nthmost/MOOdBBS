#!/usr/bin/env python3
"""
MOOdBBS Admin Tool

Shell-based administrative interface for managing MOOdBBS database and system.
"""

import os
import sys
import sqlite3
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich import box

console = Console()

DB_PATH = "data/moodbbs.db"
SCHEMA_PATH = "src/database/schema.sql"
MIGRATIONS_DIR = "src/database/migrations"


class MOOdBBSAdmin:
    """Administrative interface for MOOdBBS."""

    def __init__(self):
        self.running = True

    def show_menu(self):
        """Display the admin menu."""
        console.clear()
        console.print()
        title = "[cyan bold]MOOdBBS Admin Tool[/cyan bold]"
        console.print(Panel(title, border_style="cyan"))
        console.print()

        menu_table = Table.grid(padding=(0, 2))
        menu_table.add_column(style="yellow", justify="right")
        menu_table.add_column(style="cyan")

        menu_table.add_row("1", "Database Status")
        menu_table.add_row("2", "Reset Database (Safe)")
        menu_table.add_row("3", "Backup Database")
        menu_table.add_row("4", "View User Profile")
        menu_table.add_row("5", "Clear Active Moodlets")
        menu_table.add_row("6", "Clear Active Quests")
        menu_table.add_row("7", "View Moodlet Statistics")
        menu_table.add_row("8", "View Quest Statistics")
        menu_table.add_row("9", "Run Migrations")
        menu_table.add_row("q", "Quit")

        panel = Panel(
            menu_table,
            title="Admin Menu",
            border_style="cyan",
            box=box.ROUNDED
        )
        console.print(panel)
        console.print()

    def get_choice(self) -> str:
        """Get user menu choice."""
        choice = Prompt.ask("[yellow]Select option[/yellow]", default="q").strip().lower()
        return choice

    def database_status(self):
        """Show database status and statistics."""
        console.clear()
        console.print("\n[cyan bold]Database Status[/cyan bold]\n")

        if not os.path.exists(DB_PATH):
            console.print("[red]✗ Database does not exist[/red]")
            console.print(f"[dim]Expected location: {DB_PATH}[/dim]\n")
            Prompt.ask("[yellow]Press Enter to continue[/yellow]")
            return

        console.print(f"[green]✓ Database exists[/green]: {DB_PATH}")

        # Get file size
        size = os.path.getsize(DB_PATH)
        size_kb = size / 1024
        console.print(f"[dim]Size: {size_kb:.2f} KB[/dim]")

        # Get table counts
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            table = Table(title="Table Statistics", box=box.ROUNDED)
            table.add_column("Table", style="cyan")
            table.add_column("Records", justify="right", style="yellow")

            tables = [
                ("moodlets", "Moodlet Templates"),
                ("active_moodlets", "Active Moodlets"),
                ("quests", "Quests"),
                ("quest_completions", "Quest Completions"),
                ("mood_events", "Mood Events"),
                ("user_profile", "User Profiles"),
                ("favorite_locations", "Favorite Locations"),
            ]

            for table_name, display_name in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    table.add_row(display_name, str(count))
                except sqlite3.OperationalError:
                    table.add_row(display_name, "[dim]N/A[/dim]")

            console.print()
            console.print(table)

            # Check migrations
            cursor.execute("SELECT COUNT(*) FROM schema_migrations")
            migration_count = cursor.fetchone()[0]
            console.print(f"\n[green]✓ Applied migrations:[/green] {migration_count}")

            conn.close()

        except Exception as e:
            console.print(f"[red]Error querying database: {e}[/red]")

        console.print()
        Prompt.ask("[yellow]Press Enter to continue[/yellow]")

    def reset_database(self):
        """Reset database safely with confirmation."""
        console.clear()
        console.print("\n[yellow bold]⚠ Reset Database[/yellow bold]\n")

        if os.path.exists(DB_PATH):
            console.print("[yellow]This will:[/yellow]")
            console.print("  • Delete the current database")
            console.print("  • Create a fresh database with base schema")
            console.print("  • Apply all migrations")
            console.print("  • [red]ALL DATA WILL BE LOST[/red]")
            console.print()

            # Show what will be lost
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM quests WHERE status = 'active'")
                active_quests = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM active_moodlets")
                active_moodlets = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM quest_completions")
                completions = cursor.fetchone()[0]
                conn.close()

                console.print("[dim]Data that will be lost:[/dim]")
                console.print(f"  • {active_quests} active quests")
                console.print(f"  • {active_moodlets} active moodlets")
                console.print(f"  • {completions} quest completions")
                console.print(f"  • User profile and settings")
                console.print()
            except:
                pass

            if not Confirm.ask("[red]Are you sure you want to reset the database?[/red]", default=False):
                console.print("[green]Cancelled.[/green]")
                Prompt.ask("[yellow]Press Enter to continue[/yellow]")
                return

        console.print("\n[cyan]Resetting database...[/cyan]")

        # Backup first if exists
        if os.path.exists(DB_PATH):
            backup_path = f"{DB_PATH}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(DB_PATH, backup_path)
            console.print(f"[green]✓ Backed up to:[/green] {backup_path}")

        # Create fresh database
        try:
            # Initialize with base schema
            with open(SCHEMA_PATH, 'r') as f:
                schema_sql = f.read()

            conn = sqlite3.connect(DB_PATH)
            conn.executescript(schema_sql)
            conn.close()
            console.print("[green]✓ Created fresh database[/green]")

            # Run migrations
            console.print("[cyan]Running migrations...[/cyan]")
            result = os.system("python -m src.database.migrate")

            if result == 0:
                console.print("[green]✓ All migrations applied successfully[/green]")
            else:
                console.print("[red]✗ Migration errors occurred[/red]")

            console.print("\n[green bold]✓ Database reset complete![/green bold]")

        except Exception as e:
            console.print(f"[red]✗ Error resetting database: {e}[/red]")

        console.print()
        Prompt.ask("[yellow]Press Enter to continue[/yellow]")

    def backup_database(self):
        """Create a backup of the database."""
        console.clear()
        console.print("\n[cyan bold]Backup Database[/cyan bold]\n")

        if not os.path.exists(DB_PATH):
            console.print("[red]✗ Database does not exist[/red]")
            Prompt.ask("[yellow]Press Enter to continue[/yellow]")
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{DB_PATH}.backup.{timestamp}"

        try:
            import shutil
            shutil.copy2(DB_PATH, backup_path)
            console.print(f"[green]✓ Backup created:[/green] {backup_path}")

            size = os.path.getsize(backup_path)
            size_kb = size / 1024
            console.print(f"[dim]Size: {size_kb:.2f} KB[/dim]")

        except Exception as e:
            console.print(f"[red]✗ Backup failed: {e}[/red]")

        console.print()
        Prompt.ask("[yellow]Press Enter to continue[/yellow]")

    def view_user_profile(self):
        """View user profile information."""
        console.clear()
        console.print("\n[cyan bold]User Profile[/cyan bold]\n")

        if not os.path.exists(DB_PATH):
            console.print("[red]✗ Database does not exist[/red]")
            Prompt.ask("[yellow]Press Enter to continue[/yellow]")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_profile WHERE id = 1")
            profile = cursor.fetchone()

            if not profile:
                console.print("[yellow]No user profile found (setup not completed)[/yellow]")
            else:
                # Get column names
                col_names = [desc[0] for desc in cursor.description]

                table = Table(box=box.ROUNDED)
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="yellow")

                for col, val in zip(col_names, profile):
                    if val is not None:
                        table.add_row(col, str(val))

                console.print(table)

            conn.close()

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

        console.print()
        Prompt.ask("[yellow]Press Enter to continue[/yellow]")

    def clear_active_moodlets(self):
        """Clear all active moodlets."""
        console.clear()
        console.print("\n[yellow bold]Clear Active Moodlets[/yellow bold]\n")

        if not os.path.exists(DB_PATH):
            console.print("[red]✗ Database does not exist[/red]")
            Prompt.ask("[yellow]Press Enter to continue[/yellow]")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM active_moodlets")
            count = cursor.fetchone()[0]

            if count == 0:
                console.print("[dim]No active moodlets to clear[/dim]")
            else:
                console.print(f"[yellow]Found {count} active moodlets[/yellow]")

                if Confirm.ask("Clear all active moodlets?", default=False):
                    cursor.execute("DELETE FROM active_moodlets")
                    conn.commit()
                    console.print(f"[green]✓ Cleared {count} active moodlets[/green]")
                else:
                    console.print("[dim]Cancelled[/dim]")

            conn.close()

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

        console.print()
        Prompt.ask("[yellow]Press Enter to continue[/yellow]")

    def clear_active_quests(self):
        """Clear all active quests."""
        console.clear()
        console.print("\n[yellow bold]Clear Active Quests[/yellow bold]\n")

        if not os.path.exists(DB_PATH):
            console.print("[red]✗ Database does not exist[/red]")
            Prompt.ask("[yellow]Press Enter to continue[/yellow]")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM quests WHERE status = 'active'")
            count = cursor.fetchone()[0]

            if count == 0:
                console.print("[dim]No active quests to clear[/dim]")
            else:
                console.print(f"[yellow]Found {count} active quests[/yellow]")

                if Confirm.ask("Mark all active quests as cancelled?", default=False):
                    cursor.execute("UPDATE quests SET status = 'cancelled' WHERE status = 'active'")
                    conn.commit()
                    console.print(f"[green]✓ Cancelled {count} active quests[/green]")
                else:
                    console.print("[dim]Cancelled[/dim]")

            conn.close()

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

        console.print()
        Prompt.ask("[yellow]Press Enter to continue[/yellow]")

    def view_moodlet_stats(self):
        """View moodlet statistics."""
        console.clear()
        console.print("\n[cyan bold]Moodlet Statistics[/cyan bold]\n")

        if not os.path.exists(DB_PATH):
            console.print("[red]✗ Database does not exist[/red]")
            Prompt.ask("[yellow]Press Enter to continue[/yellow]")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Moodlets by category
            table = Table(title="Moodlets by Category", box=box.ROUNDED)
            table.add_column("Category", style="cyan")
            table.add_column("Quest-based", justify="right", style="yellow")
            table.add_column("Event-based", justify="right", style="green")
            table.add_column("Total", justify="right", style="bold")

            cursor.execute("""
                SELECT category,
                       SUM(CASE WHEN is_quest_based = 1 THEN 1 ELSE 0 END) as quest_based,
                       SUM(CASE WHEN is_quest_based = 0 THEN 1 ELSE 0 END) as event_based,
                       COUNT(*) as total
                FROM moodlets
                GROUP BY category
                ORDER BY category
            """)

            total_quest = 0
            total_event = 0
            for row in cursor.fetchall():
                category, quest_based, event_based, total = row
                table.add_row(category.title(), str(quest_based), str(event_based), str(total))
                total_quest += quest_based
                total_event += event_based

            table.add_section()
            table.add_row("[bold]TOTAL[/bold]", f"[bold]{total_quest}[/bold]",
                         f"[bold]{total_event}[/bold]", f"[bold]{total_quest + total_event}[/bold]")

            console.print(table)

            # Most applied moodlets (if any data exists)
            console.print("\n[cyan bold]Most Applied Moodlets (All Time)[/cyan bold]\n")

            cursor.execute("""
                SELECT m.name, m.category, COUNT(*) as apply_count
                FROM active_moodlets am
                JOIN moodlets m ON am.moodlet_id = m.id
                GROUP BY m.id
                ORDER BY apply_count DESC
                LIMIT 10
            """)

            results = cursor.fetchall()
            if results:
                top_table = Table(box=box.ROUNDED)
                top_table.add_column("Moodlet", style="cyan")
                top_table.add_column("Category", style="dim")
                top_table.add_column("Times Applied", justify="right", style="yellow")

                for name, category, count in results:
                    top_table.add_row(name, category.title(), str(count))

                console.print(top_table)
            else:
                console.print("[dim]No moodlet application history yet[/dim]")

            conn.close()

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

        console.print()
        Prompt.ask("[yellow]Press Enter to continue[/yellow]")

    def view_quest_stats(self):
        """View quest statistics."""
        console.clear()
        console.print("\n[cyan bold]Quest Statistics[/cyan bold]\n")

        if not os.path.exists(DB_PATH):
            console.print("[red]✗ Database does not exist[/red]")
            Prompt.ask("[yellow]Press Enter to continue[/yellow]")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Quest status breakdown
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM quests
                GROUP BY status
            """)

            table = Table(title="Quest Status", box=box.ROUNDED)
            table.add_column("Status", style="cyan")
            table.add_column("Count", justify="right", style="yellow")

            for status, count in cursor.fetchall():
                table.add_row(status.title(), str(count))

            console.print(table)

            # Completion stats
            console.print("\n[cyan bold]Completion Statistics[/cyan bold]\n")

            cursor.execute("SELECT COUNT(*) FROM quest_completions")
            total_completions = cursor.fetchone()[0]

            if total_completions > 0:
                cursor.execute("SELECT SUM(xp_earned) FROM quest_completions")
                total_xp = cursor.fetchone()[0] or 0

                cursor.execute("SELECT AVG(xp_earned) FROM quest_completions")
                avg_xp = cursor.fetchone()[0] or 0

                stats_table = Table(box=box.ROUNDED)
                stats_table.add_column("Metric", style="cyan")
                stats_table.add_column("Value", justify="right", style="yellow")

                stats_table.add_row("Total Completions", str(total_completions))
                stats_table.add_row("Total XP Earned", str(total_xp))
                stats_table.add_row("Average XP per Quest", f"{avg_xp:.1f}")

                console.print(stats_table)
            else:
                console.print("[dim]No quest completions yet[/dim]")

            conn.close()

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

        console.print()
        Prompt.ask("[yellow]Press Enter to continue[/yellow]")

    def run_migrations(self):
        """Run database migrations."""
        console.clear()
        console.print("\n[cyan bold]Run Migrations[/cyan bold]\n")

        if not os.path.exists(DB_PATH):
            console.print("[red]✗ Database does not exist[/red]")
            console.print("[yellow]Create database first (option 2)[/yellow]")
            Prompt.ask("[yellow]Press Enter to continue[/yellow]")
            return

        console.print("[cyan]Running migrations...[/cyan]\n")

        result = os.system("python -m src.database.migrate")

        if result == 0:
            console.print("\n[green]✓ Migrations completed successfully[/green]")
        else:
            console.print("\n[red]✗ Migration errors occurred[/red]")

        console.print()
        Prompt.ask("[yellow]Press Enter to continue[/yellow]")

    def run(self):
        """Main admin loop."""
        while self.running:
            self.show_menu()
            choice = self.get_choice()

            if choice == '1':
                self.database_status()
            elif choice == '2':
                self.reset_database()
            elif choice == '3':
                self.backup_database()
            elif choice == '4':
                self.view_user_profile()
            elif choice == '5':
                self.clear_active_moodlets()
            elif choice == '6':
                self.clear_active_quests()
            elif choice == '7':
                self.view_moodlet_stats()
            elif choice == '8':
                self.view_quest_stats()
            elif choice == '9':
                self.run_migrations()
            elif choice == 'q':
                self.running = False
            else:
                console.print("[red]Invalid choice[/red]")


def main():
    """Entry point for admin tool."""
    try:
        admin = MOOdBBSAdmin()
        admin.run()
        console.print("\n[cyan]Goodbye![/cyan]\n")
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/yellow]\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
