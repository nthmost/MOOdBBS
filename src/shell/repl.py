"""MOOdBBS command shell REPL."""

import sys
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.engine import MOOdBBSEngine


class MOOdBBSShell:
    """Interactive command shell for MOOdBBS."""

    def __init__(self):
        """Initialize the shell."""
        self.console = Console()
        self.engine = MOOdBBSEngine()
        self.running = True

    def run(self):
        """Run the shell REPL."""
        self.console.print("\n[bold cyan]MOOdBBS Shell v0.1.0[/bold cyan]")
        self.console.print("Type 'help' for commands, 'exit' to quit\n")

        while self.running:
            try:
                command = input("moodbbs> ").strip()
                if not command:
                    continue

                self.execute_command(command)

            except KeyboardInterrupt:
                self.console.print("\n")
                continue
            except EOFError:
                break

        self.console.print("\n[dim]Goodbye![/dim]")

    def execute_command(self, command: str):
        """Execute a shell command.

        Args:
            command: Command string to execute
        """
        parts = command.split()
        if not parts:
            return

        cmd = parts[0].lower()
        args = parts[1:]

        # Command routing
        if cmd == "help":
            self.cmd_help()
        elif cmd == "exit" or cmd == "quit":
            self.running = False
        elif cmd == "mood":
            self.cmd_mood(args)
        elif cmd == "log":
            self.cmd_log(args)
        elif cmd == "quests":
            self.cmd_quests(args)
        elif cmd == "complete":
            self.cmd_complete(args)
        elif cmd == "snooze":
            self.cmd_snooze(args)
        elif cmd == "hide":
            self.cmd_hide(args)
        elif cmd == "create":
            self.cmd_create(args)
        elif cmd == "traits":
            self.cmd_traits(args)
        elif cmd == "stats":
            self.cmd_stats()
        else:
            self.console.print(f"[red]Unknown command: {cmd}[/red]")
            self.console.print("Type 'help' for available commands")

    def cmd_help(self):
        """Show help message."""
        help_text = """
[bold]Available commands:[/bold]

[cyan]Mood System:[/cyan]
  mood                    - Show current mood
  log <event>             - Log a mood event (from library)
  log custom <name> <val> - Log custom event

[cyan]Quest System:[/cyan]
  quests                  - List active quests
  quests history          - Show completed quests
  complete <id>           - Complete a quest
  snooze <id>             - Snooze a quest
  hide <id>               - Hide a quest permanently
  create quest            - Create a new quest (interactive)

[cyan]Traits:[/cyan]
  traits                  - List active traits
  traits add <name>       - Add a trait

[cyan]General:[/cyan]
  stats                   - Show overall statistics
  help                    - Show this help
  exit                    - Exit shell
"""
        self.console.print(help_text)

    def cmd_mood(self, args: List[str]):
        """Show current mood or mood history.

        Args:
            args: Command arguments
        """
        if args and args[0] == "history":
            self.console.print("[yellow]Mood history not yet implemented[/yellow]")
            return

        mood = self.engine.get_current_mood()

        # Display mood
        mood_color = "green" if mood.score >= 10 else "yellow" if mood.score >= 0 else "red"

        self.console.print(f"\n[bold]Current Mood:[/bold] {mood.face} [{mood_color}]{mood.score:+d}[/{mood_color}]\n")

        # Show active modifiers
        if mood.active_events:
            self.console.print("[bold]Active Modifiers:[/bold]")
            for event in mood.active_events:
                modifier_color = "green" if event.modifier > 0 else "red" if event.modifier < 0 else "white"
                self.console.print(f"  [{modifier_color}]{event.modifier:+d}[/{modifier_color}] {event.event_type}")
                if event.description:
                    self.console.print(f"      [dim]{event.description}[/dim]")

        # Show traits
        if mood.active_traits:
            self.console.print("\n[bold]Active Traits:[/bold]")
            for trait in mood.active_traits:
                modifier_color = "green" if trait.mood_modifier > 0 else "red" if trait.mood_modifier < 0 else "white"
                self.console.print(f"  • {trait.trait_name} [{modifier_color}]{trait.mood_modifier:+d}[/{modifier_color}]")

        self.console.print()

    def cmd_log(self, args: List[str]):
        """Log a mood event.

        Args:
            args: Command arguments
        """
        if not args:
            # Show available modifiers
            modifiers = self.engine.get_mood_modifier_library()
            self.console.print("\n[bold]Available mood modifiers:[/bold]\n")
            for mod in modifiers:
                color = "green" if mod.default_value > 0 else "red"
                self.console.print(f"  {mod.event_type:30s} [{color}]{mod.default_value:+d}[/{color}]  {mod.name}")
            self.console.print()
            return

        if args[0] == "custom":
            # Custom event
            if len(args) < 3:
                self.console.print("[red]Usage: log custom <description> <modifier>[/red]")
                return

            # Join description parts
            description = " ".join(args[1:-1])
            try:
                modifier = int(args[-1])
            except ValueError:
                self.console.print("[red]Modifier must be a number[/red]")
                return

            event = self.engine.log_mood_event(
                event_type="custom",
                modifier=modifier,
                description=description,
                duration_hours=24
            )

            color = "green" if modifier > 0 else "red"
            self.console.print(f"[{color}]Logged: {description} ({modifier:+d})[/{color}]")

        else:
            # Stock event
            event_type = args[0]
            modifier_lib = self.engine.get_mood_modifier_library()

            # Find modifier
            modifier_def = next((m for m in modifier_lib if m.event_type == event_type), None)

            if not modifier_def:
                self.console.print(f"[red]Unknown event: {event_type}[/red]")
                self.console.print("Run 'log' with no arguments to see available events")
                return

            event = self.engine.log_mood_event(
                event_type=event_type,
                modifier=modifier_def.default_value,
                description=modifier_def.name,
                duration_hours=modifier_def.duration_hours
            )

            color = "green" if modifier_def.default_value > 0 else "red"
            self.console.print(f"[{color}]Logged: {modifier_def.name} ({modifier_def.default_value:+d})[/{color}]")

        # Show updated mood
        mood = self.engine.get_current_mood()
        mood_color = "green" if mood.score >= 10 else "yellow" if mood.score >= 0 else "red"
        self.console.print(f"Mood updated: {mood.face} [{mood_color}]{mood.score:+d}[/{mood_color}]\n")

    def cmd_quests(self, args: List[str]):
        """Show active quests or quest history.

        Args:
            args: Command arguments
        """
        if args and args[0] == "history":
            history = self.engine.get_quest_history(days=7)

            if not history:
                self.console.print("[yellow]No completed quests in the last 7 days[/yellow]")
                return

            self.console.print("\n[bold]Recently Completed Quests:[/bold]\n")
            for completion in history:
                quest = self.engine.get_quest_by_id(completion.quest_id)
                self.console.print(f"✓ {quest.title} [green]+{completion.xp_awarded} XP[/green]")
                if completion.location_visited:
                    self.console.print(f"  Location: {completion.location_visited}")
                self.console.print(f"  [dim]{completion.completed_at.strftime('%Y-%m-%d %H:%M')}[/dim]")
                self.console.print()
            return

        quests = self.engine.get_active_quests()

        if not quests:
            self.console.print("[yellow]No active quests[/yellow]")
            return

        self.console.print("\n[bold]Active Quests:[/bold]\n")
        for quest in quests:
            self.console.print(f"  {quest.id}. {quest.title} [green][{quest.xp_reward} XP][/green]")
            if quest.description:
                self.console.print(f"     {quest.description}")
            if quest.location:
                self.console.print(f"     Location: {quest.location}")
            self.console.print()

    def cmd_complete(self, args: List[str]):
        """Complete a quest.

        Args:
            args: Command arguments (quest_id)
        """
        if not args:
            self.console.print("[red]Usage: complete <quest_id>[/red]")
            return

        try:
            quest_id = int(args[0])
        except ValueError:
            self.console.print("[red]Quest ID must be a number[/red]")
            return

        try:
            result = self.engine.complete_quest(quest_id)

            self.console.print(f"\n[green]Quest completed! +{result.xp_awarded} XP[/green]")
            self.console.print(f"Total XP: {result.total_xp}\n")

            self.console.print("Mood buffs applied:")
            for event_type, modifier in result.mood_buffs_applied:
                color = "green" if modifier > 0 else "red"
                self.console.print(f"  [{color}]{modifier:+d}[/{color}] {event_type}")

            # Ask about additional modifiers
            self.console.print("\nLog additional modifiers? (y/n): ", end="")
            response = input().strip().lower()

            if response == "y":
                self._prompt_additional_modifiers(quest_id)

            # Show updated mood
            mood = self.engine.get_current_mood()
            mood_color = "green" if mood.score >= 10 else "yellow" if mood.score >= 0 else "red"
            self.console.print(f"\nMood updated: {mood.face} [{mood_color}]{mood.score:+d}[/{mood_color}]\n")

        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _prompt_additional_modifiers(self, quest_id: int):
        """Prompt for additional mood modifiers after quest completion.

        Args:
            quest_id: Completed quest ID
        """
        self.console.print("\nQuick options:")
        self.console.print("  1. Pain (-)")
        self.console.print("  2. Energized (+)")
        self.console.print("  3. Beautiful view (+4)")
        self.console.print("  4. Social interaction (+8)")
        self.console.print("  5. Custom...")
        self.console.print("  d. Done")

        while True:
            choice = input("\nSelect: ").strip().lower()

            if choice == "d" or choice == "":
                break
            elif choice == "1":
                severity = input("Pain severity (1-10): ").strip()
                try:
                    val = -int(severity)
                    self.engine.log_mood_event("pain", val, "Pain", duration_hours=24)
                    self.console.print(f"[red]Added: Pain ({val})[/red]")
                except ValueError:
                    self.console.print("[red]Invalid number[/red]")
            elif choice == "2":
                level = input("Energy level (1-10): ").strip()
                try:
                    val = int(level)
                    self.engine.log_mood_event("energized", val, "Energized", duration_hours=12)
                    self.console.print(f"[green]Added: Energized (+{val})[/green]")
                except ValueError:
                    self.console.print("[red]Invalid number[/red]")
            elif choice == "3":
                self.engine.log_mood_event("beautiful_view", 4, "Beautiful view", duration_hours=12)
                self.console.print("[green]Added: Beautiful view (+4)[/green]")
            elif choice == "4":
                self.engine.log_mood_event("social_interaction", 8, "Social interaction", duration_hours=24)
                self.console.print("[green]Added: Social interaction (+8)[/green]")
            elif choice == "5":
                desc = input("Description: ").strip()
                mod = input("Modifier: ").strip()
                try:
                    val = int(mod)
                    self.engine.log_mood_event("custom", val, desc, duration_hours=24)
                    color = "green" if val > 0 else "red"
                    self.console.print(f"[{color}]Added: {desc} ({val:+d})[/{color}]")
                except ValueError:
                    self.console.print("[red]Invalid modifier[/red]")

    def cmd_snooze(self, args: List[str]):
        """Snooze a quest.

        Args:
            args: Command arguments (quest_id)
        """
        if not args:
            self.console.print("[red]Usage: snooze <quest_id>[/red]")
            return

        try:
            quest_id = int(args[0])
        except ValueError:
            self.console.print("[red]Quest ID must be a number[/red]")
            return

        try:
            quest = self.engine.get_quest_by_id(quest_id)
            self.console.print(f"\nQuest snoozed: \"{quest.title}\"")

            # Ask for reason
            self.console.print("\nWhy not now? (Enter to skip)")
            self.console.print("  1. Weather")
            self.console.print("  2. Don't have time")
            self.console.print("  3. Not in the mood")
            self.console.print("  4. Other (specify)")

            choice = input("\nSelect (or Enter): ").strip()

            reason_category = "unspecified"
            reason_text = None

            if choice == "1":
                reason_category = "weather"
                reason_text = "Weather"
            elif choice == "2":
                reason_category = "time"
                reason_text = "Don't have time"
            elif choice == "3":
                reason_category = "mood"
                reason_text = "Not in the mood"
            elif choice == "4":
                reason_text = input("Other reason: ").strip()
                reason_category = "other"

            self.engine.snooze_quest(
                quest_id=quest_id,
                reason_category=reason_category,
                reason_text=reason_text
            )

            self.console.print("\n[green]Noted! Snoozed for 7 days.[/green]\n")

        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def cmd_hide(self, args: List[str]):
        """Hide a quest permanently.

        Args:
            args: Command arguments (quest_id)
        """
        if not args:
            self.console.print("[red]Usage: hide <quest_id>[/red]")
            return

        try:
            quest_id = int(args[0])
            quest = self.engine.get_quest_by_id(quest_id)

            self.console.print(f"\nHide quest permanently: \"{quest.title}\"?")
            confirm = input("Type 'yes' to confirm: ").strip().lower()

            if confirm == "yes":
                self.engine.hide_quest(quest_id)
                self.console.print("[green]Quest hidden permanently[/green]\n")
            else:
                self.console.print("[yellow]Cancelled[/yellow]\n")

        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def cmd_create(self, args: List[str]):
        """Create a new quest interactively.

        Args:
            args: Command arguments
        """
        if not args or args[0] != "quest":
            self.console.print("[red]Usage: create quest[/red]")
            return

        self.console.print("\n[bold]Create New Quest[/bold]\n")

        title = input("Title: ").strip()
        if not title:
            self.console.print("[red]Title required[/red]")
            return

        description = input("Description (optional): ").strip()
        location = input("Location (optional): ").strip()

        self.console.print("\nCategory:")
        self.console.print("  1. Social")
        self.console.print("  2. Constitutional")
        self.console.print("  3. Creative")
        self.console.print("  4. Experiential")
        cat_choice = input("Select: ").strip()

        category_map = {"1": "social", "2": "constitutional", "3": "creative", "4": "experiential"}
        category = category_map.get(cat_choice, "experiential")

        self.console.print("\nDifficulty:")
        self.console.print("  1. Easy (5-10 XP)")
        self.console.print("  2. Medium (15-20 XP)")
        self.console.print("  3. Hard (25-35 XP)")
        self.console.print("  4. Extreme (40-50 XP)")
        diff_choice = input("Select: ").strip()

        difficulty_map = {
            "1": ("easy", 10),
            "2": ("medium", 18),
            "3": ("hard", 30),
            "4": ("extreme", 50)
        }
        difficulty, xp = difficulty_map.get(diff_choice, ("easy", 10))

        try:
            quest = self.engine.create_quest(
                title=title,
                description=description,
                category=category,
                difficulty=difficulty,
                location=location,
                xp_reward=xp
            )

            self.console.print(f"\n[green]Quest created! Added to active quests.[/green]")
            self.console.print(f"{quest.id}. {quest.title} [{xp} XP]\n")

        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def cmd_traits(self, args: List[str]):
        """Show or manage traits.

        Args:
            args: Command arguments
        """
        if not args:
            traits = self.engine.get_active_traits()

            if not traits:
                self.console.print("[yellow]No active traits[/yellow]")
                return

            self.console.print("\n[bold]Active Traits:[/bold]\n")
            for trait in traits:
                modifier_color = "green" if trait.mood_modifier > 0 else "red" if trait.mood_modifier < 0 else "white"
                self.console.print(f"  • {trait.trait_name} [{modifier_color}]{trait.mood_modifier:+d}[/{modifier_color}]")
                if trait.description:
                    self.console.print(f"    [dim]{trait.description}[/dim]")
            self.console.print()
            return

        if args[0] == "add":
            if len(args) < 2:
                self.console.print("[red]Usage: traits add <trait_name>[/red]")
                return

            trait_name = " ".join(args[1:])
            description = input("Description (optional): ").strip()
            modifier_str = input("Mood modifier: ").strip()

            try:
                modifier = int(modifier_str)
                trait = self.engine.add_trait(trait_name, description, modifier)
                color = "green" if modifier > 0 else "red"
                self.console.print(f"[{color}]Trait added: {trait_name} ({modifier:+d})[/{color}]\n")
            except ValueError:
                self.console.print("[red]Modifier must be a number[/red]")

    def cmd_stats(self):
        """Show overall statistics."""
        stats = self.engine.get_user_stats()

        self.console.print("\n[bold]MOOdBBS Statistics[/bold]\n")
        self.console.print(f"Total XP:          {stats['total_xp']}")
        self.console.print(f"Quests Completed:  {stats['quests_completed']}")

        mood_color = "green" if stats['current_mood'] >= 10 else "yellow" if stats['current_mood'] >= 0 else "red"
        self.console.print(f"Current Mood:      [{mood_color}]{stats['current_mood']:+d}[/{mood_color}]")

        self.console.print(f"Active Traits:     {stats['active_traits']}")
        self.console.print(f"Active Modifiers:  {stats['active_modifiers']}\n")


def main():
    """Main entry point for the shell."""
    shell = MOOdBBSShell()
    shell.run()


if __name__ == "__main__":
    main()
