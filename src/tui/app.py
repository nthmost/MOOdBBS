"""Main TUI application for MOOdBBS."""

from src.engine import MOOdBBSEngine
from src.tui.screens import (
    BootScreen,
    MainMenuScreen,
    MoodStatsScreen,
    WanderMOOScreen,
    QuickLogScreen,
    AboutScreen,
    SettingsScreen,
    SetupWizardScreen,
)


class MOOdBBSApp:
    """Main TUI application."""

    def __init__(self):
        self.engine = MOOdBBSEngine()
        self.running = True

        # Initialize screens
        self.boot_screen = BootScreen()
        self.setup_wizard = SetupWizardScreen(self.engine)
        self.main_menu = MainMenuScreen()
        self.mood_stats = MoodStatsScreen(self.engine)
        self.wander_moo = WanderMOOScreen(self.engine)
        self.quick_log = QuickLogScreen(self.engine)
        self.about = AboutScreen()
        self.settings = SettingsScreen(self.engine)

    def run(self):
        """Run the TUI application."""
        # Show boot screen
        self.boot_screen.show()

        # Check if first run
        profile = self.engine.db.get_user_profile()
        if not profile.setup_completed:
            self.setup_wizard.show()

        # Main menu loop
        while self.running:
            self.main_menu.show()
            choice = self.main_menu.get_choice()

            if choice == '1':
                self.wander_moo.show()
            elif choice == '2':
                self.mood_stats.show()
            elif choice == '3':
                self.quick_log.show()
            elif choice == '4':
                self.settings.show()
            elif choice == '5':
                self.about.show()
            elif choice == 'q':
                self.running = False

        # Goodbye message
        from rich.console import Console
        from rich.align import Align
        console = Console()
        console.clear()
        console.print()
        console.print(Align.center("Disconnecting from MOOdBBS...", style="yellow"))
        console.print()
        console.print(Align.center("Goodbye!", style="cyan bold"))
        console.print()


def main():
    """Entry point for TUI."""
    app = MOOdBBSApp()
    app.run()


if __name__ == "__main__":
    main()
