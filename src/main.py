"""Main application entry point for MOOdBBS."""

import sys
from pathlib import Path
from rich.console import Console

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db.models import Database
from src.ui.main_menu import render_connection_screen, render_dashboard, render_main_menu


class MOOdBBS:
    """Main application controller for MOOdBBS."""

    def __init__(self):
        """Initialize MOOdBBS application."""
        self.console = Console()
        self.db = Database("data/moodbbs.db")
        self.current_screen = "boot"
        self.running = True

    def run(self):
        """Main application loop."""
        # Show boot screen
        render_connection_screen(self.console)
        input()  # Wait for ENTER

        # Initialize some sample data if database is empty
        self._init_sample_data()

        # Main loop
        while self.running:
            if self.current_screen == "boot":
                self.show_dashboard()
                self.current_screen = "dashboard"
            elif self.current_screen == "dashboard":
                self.show_dashboard()
                self.handle_dashboard_input()
            elif self.current_screen == "menu":
                self.show_menu()
                self.handle_menu_input()

    def show_dashboard(self):
        """Display the main dashboard."""
        mood_score = self.db.calculate_current_mood()
        quests = self.db.get_active_quests(limit=3)
        events = self.db.get_active_mood_events()

        # Determine mood face
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

        render_dashboard(self.console, mood_score, mood_face, quests, events)

    def show_menu(self):
        """Display the main menu."""
        self.console.clear()
        render_main_menu(self.console)

    def handle_dashboard_input(self):
        """Handle input from dashboard screen."""
        key = input("\nEnter choice (1-5, or 'm' for menu): ").strip()

        if key == "m" or key == "M":
            self.current_screen = "menu"
        elif key == "1":
            self.show_wandermoo()
        elif key == "2":
            self.show_moodstats()
        elif key == "3":
            self.show_log_action()
        elif key == "4":
            self.show_settings()
        elif key == "5":
            self.show_about()
        elif key == "q" or key == "Q":
            self.running = False

    def handle_menu_input(self):
        """Handle input from menu screen."""
        key = input("\nEnter choice (1-5): ").strip()

        if key == "1":
            self.show_wandermoo()
        elif key == "2":
            self.show_moodstats()
        elif key == "3":
            self.show_log_action()
        elif key == "4":
            self.show_settings()
        elif key == "5":
            self.show_about()
        elif key == "q" or key == "Q":
            self.running = False
        else:
            self.current_screen = "dashboard"

    def show_wandermoo(self):
        """Show WanderMOO quest interface."""
        self.console.clear()
        self.console.print("[bold cyan]WanderMOO - Quest System[/bold cyan]\n")

        quests = self.db.get_active_quests(limit=10)

        if not quests:
            self.console.print("[yellow]No active quests available.[/yellow]")
            self.console.print("\n[dim]Press ENTER to return[/dim]")
            input()
            self.current_screen = "dashboard"
            return

        for i, quest in enumerate(quests, 1):
            self.console.print(f"[bold yellow]{i}. {quest['title']}[/bold yellow]")
            if quest.get('description'):
                self.console.print(f"   {quest['description']}")
            if quest.get('location'):
                self.console.print(f"   Location: {quest['location']}", style="cyan")
            self.console.print(f"   XP Reward: {quest['xp_reward']}", style="green")
            self.console.print()

        choice = input("\nComplete quest # (or ENTER to return): ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(quests):
            quest_id = quests[int(choice) - 1]['id']
            if self.db.complete_quest(quest_id):
                self.console.print("[green]Quest completed! +XP[/green]")

                # Ask if they want to log mood
                log_mood = input("Log mood related to this quest? (y/n): ").strip().lower()
                if log_mood == 'y':
                    self.current_screen = "log_action"
                    return

        self.current_screen = "dashboard"

    def show_moodstats(self):
        """Show mood statistics and active modifiers."""
        self.console.clear()
        self.console.print("[bold cyan]MoodStats - Current Status[/bold cyan]\n")

        mood_score = self.db.calculate_current_mood()
        events = self.db.get_active_mood_events()
        traits = self.db.get_active_traits()

        # Show current mood
        mood_color = "green" if mood_score >= 10 else "yellow" if mood_score >= 0 else "red"
        self.console.print(f"Current Mood Score: [{mood_color}]{mood_score:+d}[/{mood_color}]\n")

        # Show active traits
        if traits:
            self.console.print("[bold]Active Traits:[/bold]")
            for trait in traits:
                modifier_color = "green" if trait['mood_modifier'] > 0 else "red" if trait['mood_modifier'] < 0 else "white"
                self.console.print(f"  • {trait['trait_name']} [{modifier_color}]{trait['mood_modifier']:+d}[/{modifier_color}]")
            self.console.print()

        # Show active modifiers
        if events:
            self.console.print("[bold]Active Modifiers:[/bold]")
            for event in events:
                modifier_color = "green" if event['modifier'] > 0 else "red" if event['modifier'] < 0 else "white"
                self.console.print(f"  [{modifier_color}]{event['modifier']:+d}[/{modifier_color}] {event['event_type']}")
                if event.get('description'):
                    self.console.print(f"      {event['description']}", style="dim")
        else:
            self.console.print("[yellow]No active modifiers[/yellow]")

        self.console.print("\n[dim]Press ENTER to return[/dim]")
        input()
        self.current_screen = "dashboard"

    def show_log_action(self):
        """Show manual mood event logging interface."""
        self.console.clear()
        self.console.print("[bold cyan]LogAction - Manual Mood Entry[/bold cyan]\n")

        # Sample common events (we'll expand this later)
        self.console.print("Common Events:")
        self.console.print("  1. Ate without table (-3)")
        self.console.print("  2. Had a fine meal (+5)")
        self.console.print("  3. Social interaction (+8)")
        self.console.print("  4. Completed a walk (+6)")
        self.console.print("  5. Too long indoors (-5)")
        self.console.print("  6. Saw something beautiful (+4)")
        self.console.print("  7. Custom event")

        choice = input("\nSelect event (1-7 or ENTER to cancel): ").strip()

        event_map = {
            "1": ("ate_without_table", -3, "Ate without table"),
            "2": ("fine_meal", 5, "Had a fine meal"),
            "3": ("social_interaction", 8, "Social interaction"),
            "4": ("completed_walk", 6, "Completed a walk"),
            "5": ("too_long_indoors", -5, "Too long indoors"),
            "6": ("saw_beauty", 4, "Saw something beautiful"),
        }

        if choice in event_map:
            event_type, modifier, description = event_map[choice]
            self.db.add_mood_event(event_type, modifier, description, duration_hours=24)
            self.console.print(f"[green]Logged: {description} ({modifier:+d})[/green]")
            input("\nPress ENTER to continue...")
        elif choice == "7":
            desc = input("Event description: ").strip()
            modifier_str = input("Modifier (+/-): ").strip()
            try:
                modifier = int(modifier_str)
                self.db.add_mood_event("custom", modifier, desc, duration_hours=24)
                self.console.print(f"[green]Logged: {desc} ({modifier:+d})[/green]")
                input("\nPress ENTER to continue...")
            except ValueError:
                self.console.print("[red]Invalid modifier[/red]")
                input("\nPress ENTER to continue...")

        self.current_screen = "dashboard"

    def show_settings(self):
        """Show settings interface."""
        self.console.clear()
        self.console.print("[bold cyan]Settings[/bold cyan]\n")
        self.console.print("[yellow]Settings not yet implemented[/yellow]")
        self.console.print("\n[dim]Press ENTER to return[/dim]")
        input()
        self.current_screen = "dashboard"

    def show_about(self):
        """Show about screen."""
        self.console.clear()
        self.console.print("[bold cyan]About MOOdBBS[/bold cyan]\n")
        self.console.print("MOOdBBS v0.1.0")
        self.console.print("A RimWorld-inspired mood tracker with 90s BBS aesthetics")
        self.console.print("\ni made this with my own hooves 🐴")
        self.console.print("\n[dim]Press ENTER to return[/dim]")
        input()
        self.current_screen = "dashboard"

    def _init_sample_data(self):
        """Initialize sample data if database is empty."""
        if not self.db.get_active_quests():
            # Add some sample quests
            self.db.add_quest(
                "Visit Coit Tower before sunset",
                "Go to Coit Tower and enjoy the view before 4pm",
                "Coit Tower, Telegraph Hill",
                xp_reward=15,
                due_hours=6
            )
            self.db.add_quest(
                "Get coffee at a new cafe",
                "Try a cafe you've never been to before",
                "Somewhere in SF",
                xp_reward=10
            )
            self.db.add_quest(
                "Walk to the ocean",
                "Take a bike or walk to Ocean Beach",
                "Ocean Beach",
                xp_reward=20
            )

        # Add a sample trait if none exist
        if not self.db.get_active_traits():
            self.db.add_trait("Optimist", "Natural mood boost", mood_modifier=5)

        # Add a sample mood event if none exist
        if not self.db.get_active_mood_events():
            self.db.add_mood_event("started_moodbbs", 10, "Started using MOOdBBS!", duration_hours=48)

    def cleanup(self):
        """Clean up resources."""
        self.db.save_mood_snapshot()
        self.db.close()


def main():
    """Main entry point."""
    app = MOOdBBS()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    finally:
        app.cleanup()


if __name__ == "__main__":
    main()
