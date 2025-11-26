"""TUI screens for MOOdBBS using Rich."""

import time
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.table import Table
from rich import box

from src.services.zipcode_validator import ZipcodeValidator

console = Console()
zipcode_validator = ZipcodeValidator()


class BootScreen:
    """BBS-style connection screen with ASCII art."""

    COW_ART = r"""
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
    """

    def show(self):
        """Display boot sequence."""
        console.clear()

        # ASCII cow
        cow_text = Text(self.COW_ART, style="cyan")
        console.print(Align.center(cow_text))
        console.print()

        # Connecting animation
        console.print(Align.center("Connecting to MOOdBBS...", style="yellow"))
        time.sleep(0.5)

        console.print(Align.center("CONNECT 2400", style="green bold"))
        time.sleep(0.8)

        console.print()
        console.print(Align.center("Welcome to MOOdBBS", style="cyan bold"))
        console.print(Align.center("Your mood. Your quests. Your world.", style="dim"))
        console.print()
        time.sleep(1)


class MainMenuScreen:
    """Main menu with 5 options."""

    MENU_OPTIONS = [
        ("1", "WanderMOO", "View and manage your quests"),
        ("2", "MoodStats", "Check your current mood and traits"),
        ("3", "LogAction", "Log a mood-affecting event"),
        ("4", "Settings", "Configure MOOdBBS"),
        ("5", "About", "About this system"),
        ("q", "Quit", "Exit MOOdBBS"),
    ]

    def show(self):
        """Display main menu."""
        console.clear()

        # Title
        title = Text("MOOdBBS Main Menu", style="cyan bold")
        console.print()
        console.print(Align.center(title))
        console.print()

        # Menu box
        menu_table = Table.grid(padding=(0, 2))
        menu_table.add_column(style="yellow", justify="right")
        menu_table.add_column(style="cyan bold")
        menu_table.add_column(style="dim")

        for key, name, desc in self.MENU_OPTIONS:
            menu_table.add_row(f"  {key}  ", name, desc)

        panel = Panel(
            Align.center(menu_table),
            box=box.DOUBLE,
            border_style="cyan",
            padding=(1, 2)
        )

        console.print(Align.center(panel))
        console.print()

    def get_choice(self) -> str:
        """Get user menu choice."""
        while True:
            choice = console.input("[yellow]Select option (1-5, q=quit):[/yellow] ").strip().lower()
            valid_choices = [opt[0] for opt in self.MENU_OPTIONS]
            if choice in valid_choices:
                return choice
            console.print("[red]Invalid choice. Please enter 1-5 or q.[/red]")


class MoodStatsScreen:
    """Display current mood, traits, and recent modifiers."""

    def __init__(self, engine):
        self.engine = engine

    def show(self):
        """Display mood statistics."""
        console.clear()

        # Title
        console.print()
        console.print(Align.center(Text("MoodStats", style="cyan bold")))
        console.print()

        # Get current mood (MoodState object)
        mood_state = self.engine.get_current_mood()

        # Mood display
        mood_text = Text()
        mood_text.append("Current Mood: ", style="white")
        mood_text.append(f"{mood_state.face} ", style="yellow bold")
        mood_text.append(f"{mood_state.score:+d}", style="cyan")

        console.print(Align.center(mood_text))
        console.print()

        # Active traits
        if mood_state.active_traits:
            console.print("[cyan bold]Active Traits:[/cyan bold]")
            for trait in mood_state.active_traits:
                mod_style = "green" if trait.mood_modifier >= 0 else "red"
                console.print(f"  [{mod_style}]{trait.mood_modifier:+d}[/{mod_style}] {trait.trait_name}")
                console.print(f"      [dim]{trait.description}[/dim]")
            console.print()

        # Active modifiers (MoodEvent objects)
        if mood_state.active_events:
            console.print("[cyan bold]Active Modifiers:[/cyan bold]")
            for event in mood_state.active_events:
                mod_style = "green" if event.modifier >= 0 else "red"
                console.print(f"  [{mod_style}]{event.modifier:+d}[/{mod_style}] {event.event_type}")
                console.print(f"      [dim]{event.description}[/dim]")
        else:
            console.print("[dim]No active mood modifiers[/dim]")

        console.print()
        console.input("[yellow]Press Enter to return to menu...[/yellow]")


class WanderMOOScreen:
    """Quest management interface."""

    def __init__(self, engine):
        self.engine = engine

    def show(self):
        """Display quest list and management options."""
        while True:
            console.clear()

            # Title
            console.print()
            console.print(Align.center(Text("WanderMOO - Quest System", style="cyan bold")))
            console.print()

            # Get active quests
            quests = self.engine.get_active_quests()

            if not quests:
                console.print("[dim]No active quests. Create one to get started![/dim]")
                console.print()
            else:
                console.print("[cyan bold]Active Quests:[/cyan bold]")
                for quest in quests:
                    xp_style = "yellow" if quest.xp_reward <= 10 else "green" if quest.xp_reward <= 20 else "red"
                    console.print(f"  [{quest.id}] {quest.title} [{xp_style}]{quest.xp_reward} XP[/{xp_style}]")
                    console.print(f"      [dim]{quest.description}[/dim]")

                    # Show category, renewal, and constraint info
                    renewal_info = quest.renewal_policy.renewal_type if quest.renewal_policy else "one-time"
                    info_parts = [quest.category.title(), renewal_info]

                    if quest.constraint_note:
                        info_parts.append(f"[{quest.constraint_note}]")

                    console.print(f"      [dim]{' | '.join(info_parts)}[/dim]")
                console.print()

            # Options
            console.print("[yellow]Options:[/yellow]")
            console.print("  [cyan bold]c[/cyan bold] - Create new quest")
            console.print("  [cyan bold]x[/cyan bold] - Complete quest")
            console.print("  [cyan bold]s[/cyan bold] - Snooze quest")
            console.print("  [cyan bold]h[/cyan bold] - View history")
            console.print("  [cyan bold]m[/cyan bold] - Manage quests")
            console.print("  [cyan bold]b[/cyan bold] - Back to menu")
            console.print()

            choice = console.input("[yellow]Enter choice (c/x/s/h/m/b):[/yellow] ").strip().lower()

            if choice == 'b':
                break
            elif choice == 'c':
                self._create_quest()
            elif choice == 'x':
                self._complete_quest(quests)
            elif choice == 's':
                self._snooze_quest(quests)
            elif choice == 'h':
                self._show_history()
            elif choice == 'm':
                self._manage_quests(quests)

    def _create_quest(self):
        """Interactive quest creation."""
        console.print()
        console.print("[cyan bold]Create New Quest[/cyan bold]")
        console.print()

        # Check if LLM is available
        from src.services.llm_quest_parser import LLMQuestParser
        llm_parser = LLMQuestParser()
        llm_available = llm_parser.is_available()

        if llm_available:
            console.print("[cyan bold]Mode:[/cyan bold]")
            console.print("  [cyan bold]1[/cyan bold]. Smart mode (describe in your own words)")
            console.print("  [cyan bold]2[/cyan bold]. Manual mode (step-by-step)")
            mode_choice = console.input("[yellow]Select mode (1-2):[/yellow] ").strip()

            if mode_choice == '1':
                self._create_quest_smart(llm_parser)
                return

        # Fall through to manual mode
        console.print()
        console.print("[yellow]Manual Quest Creation[/yellow]")
        console.print()

        title = console.input("Title: ").strip()
        if not title:
            console.print("[red]Cancelled[/red]")
            time.sleep(1)
            return

        description = console.input("Description: ").strip()

        # Category selection
        console.print()
        console.print("[cyan bold]Category:[/cyan bold]")
        categories = ["social", "constitutional", "creative", "experiential"]
        for i, cat in enumerate(categories, 1):
            console.print(f"  [cyan bold]{i}[/cyan bold]. {cat.title()}")

        cat_choice = console.input("[yellow]Select category (1-4):[/yellow] ").strip()
        try:
            category = categories[int(cat_choice) - 1]
        except (ValueError, IndexError):
            console.print("[red]Invalid category[/red]")
            time.sleep(1)
            return

        # Difficulty selection
        console.print()
        console.print("[cyan bold]Difficulty:[/cyan bold]")
        console.print("  [cyan bold]1[/cyan bold]. Easy (5-10 XP)")
        console.print("  [cyan bold]2[/cyan bold]. Medium (15-20 XP)")
        console.print("  [cyan bold]3[/cyan bold]. Hard (25-35 XP)")
        console.print("  [cyan bold]4[/cyan bold]. Extreme (40-50 XP)")

        diff_choice = console.input("[yellow]Select difficulty (1-4):[/yellow] ").strip()
        difficulty_map = {"1": 10, "2": 20, "3": 30, "4": 45}
        xp_reward = difficulty_map.get(diff_choice, 10)

        # Renewal policy
        console.print()
        console.print("[cyan bold]Quest Type:[/cyan bold]")
        console.print("  [cyan bold]1[/cyan bold]. One-time quest")
        console.print("  [cyan bold]2[/cyan bold]. Repeatable quest")

        renewal_choice = console.input("[yellow]Select type (1-2):[/yellow] ").strip()

        renewal_policy = None
        if renewal_choice == '2':
            # Ask for renewal frequency
            console.print()
            console.print("[cyan bold]How often should this quest renew?[/cyan bold]")
            console.print("  [cyan bold]1[/cyan bold]. Daily")
            console.print("  [cyan bold]2[/cyan bold]. Weekly")
            console.print("  [cyan bold]3[/cyan bold]. Monthly")
            console.print("  [cyan bold]4[/cyan bold]. Seasonal (3 months)")

            freq_choice = console.input("[yellow]Select frequency (1-4):[/yellow] ").strip()

            from src.domain.quests import RenewalPolicy

            if freq_choice == '1':
                renewal_policy = RenewalPolicy(renewal_type="daily", cooldown_days=1)
            elif freq_choice == '2':
                renewal_policy = RenewalPolicy(renewal_type="weekly", cooldown_days=7)
            elif freq_choice == '3':
                renewal_policy = RenewalPolicy(renewal_type="monthly", cooldown_days=30)
            elif freq_choice == '4':
                renewal_policy = RenewalPolicy(renewal_type="seasonal", cooldown_days=90)

        # Time constraints
        console.print()
        console.print("[cyan bold]Does this quest have time constraints?[/cyan bold]")
        console.print("  [cyan bold]1[/cyan bold]. No, available anytime")
        console.print("  [cyan bold]2[/cyan bold]. Only on specific day(s) of week")
        console.print("  [cyan bold]3[/cyan bold]. Only on specific day(s) of month")

        constraint_choice = console.input("[yellow]Select constraint (1-3):[/yellow] ").strip()

        constraint_type = None
        constraint_note = None

        if constraint_choice == '2':
            # Day of week constraint
            console.print()
            console.print("[cyan bold]Which day(s) of the week?[/cyan bold]")
            console.print("  Examples: 'Friday', 'Mon,Wed,Fri', 'Saturday,Sunday'")
            days = console.input("[yellow]Enter day(s):[/yellow] ").strip()
            if days:
                constraint_type = "day_of_week"
                constraint_note = days

        elif constraint_choice == '3':
            # Day of month constraint
            console.print()
            console.print("[cyan bold]Which day(s) of the month?[/cyan bold]")
            console.print("  Examples: '1' (first), '15' (mid-month), '1,15' (twice monthly)")
            console.print("  Special: 'first_friday', 'last_saturday', etc.")
            days = console.input("[yellow]Enter day(s) or pattern:[/yellow] ").strip()
            if days:
                constraint_type = "day_of_month"
                constraint_note = days

        # Create quest
        quest = self.engine.create_quest(
            title=title,
            description=description,
            category=category,
            difficulty="easy" if xp_reward <= 10 else "medium" if xp_reward <= 20 else "hard",
            xp_reward=xp_reward,
            renewal_policy=renewal_policy,
            constraint_type=constraint_type,
            constraint_note=constraint_note
        )

        console.print()
        renewal_msg = f" ({renewal_policy.renewal_type})" if renewal_policy else " (one-time)"
        constraint_msg = f" [{constraint_note}]" if constraint_note else ""
        console.print(f"[green]Quest created! [{quest.id}] {quest.title}{renewal_msg}{constraint_msg}[/green]")
        time.sleep(1.5)

    def _create_quest_smart(self, llm_parser):
        """Create quest using LLM parsing."""
        console.print()
        console.print("[cyan bold]Smart Quest Creation[/cyan bold]")
        console.print("[dim]Describe your quest in natural language...[/dim]")
        console.print()

        user_input = console.input("[yellow]Quest:[/yellow] ").strip()
        if not user_input:
            console.print("[red]Cancelled[/red]")
            time.sleep(1)
            return

        console.print()
        console.print("[yellow]Parsing with LLM...[/yellow]")

        # Get user profile for context
        user_profile = self.engine.db.get_user_profile()
        user_context = user_profile.get_context_for_llm()

        quest_data = llm_parser.parse_quest(user_input, user_context)

        if not quest_data:
            console.print("[red]Could not parse quest. Falling back to manual mode.[/red]")
            time.sleep(2)
            return

        # Apply user profile adjustments to XP
        base_xp = quest_data['xp_reward']
        adjusted_xp = base_xp
        xp_notes = []

        user_profile = self.engine.db.get_user_profile()
        if user_profile.memberships:
            # Check if quest location matches any membership
            quest_title = quest_data['title'].lower()
            for membership in user_profile.memberships:
                if membership.lower() in quest_title:
                    adjusted_xp = max(5, int(base_xp * 0.7))  # 30% reduction, minimum 5 XP
                    xp_notes.append(f"Easy access! Adjusted from {base_xp} (no admission cost with {membership} membership)")
                    break

        quest_data['xp_reward'] = adjusted_xp

        # Show parsed data for confirmation
        console.print()
        console.print("[cyan bold]Parsed Quest:[/cyan bold]")
        console.print(f"  Title: {quest_data['title']}")
        console.print(f"  Description: {quest_data.get('description', 'N/A')}")
        console.print(f"  Category: {quest_data['category']}")
        console.print(f"  XP Reward: {quest_data['xp_reward']}")
        if xp_notes:
            for note in xp_notes:
                console.print(f"    [dim]{note}[/dim]")

        renewal_type = quest_data.get('renewal_type')
        if renewal_type:
            console.print(f"  Renewal: {renewal_type}")

        constraint_note = quest_data.get('constraint_note')
        if constraint_note:
            console.print(f"  Constraint: {constraint_note}")

        time_note = quest_data.get('time_note')
        if time_note:
            console.print(f"  [dim]Time: {time_note}[/dim]")

        console.print()

        # Ask about renewal frequency if the LLM suggested one
        if renewal_type:
            console.print("[yellow]How often would you like to do this?[/yellow]")
            console.print(f"  [cyan bold]1[/cyan bold]. One-time only")
            console.print(f"  [cyan bold]2[/cyan bold]. Daily")
            console.print(f"  [cyan bold]3[/cyan bold]. Weekly")
            console.print(f"  [cyan bold]4[/cyan bold]. Monthly")
            console.print(f"  [cyan bold]5[/cyan bold]. Seasonal (every 3 months)")
            console.print(f"  [cyan bold]6[/cyan bold]. Use suggested ({renewal_type})")

            renewal_choice = console.input("[yellow]Select (1-6):[/yellow] ").strip()

            renewal_map = {
                "1": None,
                "2": "daily",
                "3": "weekly",
                "4": "monthly",
                "5": "seasonal",
                "6": renewal_type  # Keep LLM suggestion
            }

            renewal_type = renewal_map.get(renewal_choice, renewal_type)
            quest_data['renewal_type'] = renewal_type

            if renewal_type:
                console.print(f"  → Set to [cyan]{renewal_type}[/cyan]")
            else:
                console.print(f"  → Set to [cyan]one-time[/cyan]")
            console.print()

        # Review and edit loop
        while True:
            console.print("[yellow]Options:[/yellow]")
            console.print("  [cyan bold]y[/cyan bold] - Create this quest")
            console.print("  [cyan bold]e[/cyan bold] - Edit XP or category")
            console.print("  [cyan bold]n[/cyan bold] - Cancel")
            console.print()

            confirm = console.input("[yellow]Select (y/e/n):[/yellow] ").strip().lower()

            if confirm == 'n':
                console.print("[dim]Cancelled[/dim]")
                time.sleep(1)
                return
            elif confirm == 'e':
                # Edit mode
                console.print()
                console.print("[yellow]What would you like to edit?[/yellow]")
                console.print("  [cyan bold]1[/cyan bold] - XP reward (currently {})".format(quest_data['xp_reward']))
                console.print("  [cyan bold]2[/cyan bold] - Category (currently {})".format(quest_data['category']))
                console.print("  [cyan bold]3[/cyan bold] - Title (currently {})".format(quest_data['title']))
                console.print("  [cyan bold]b[/cyan bold] - Back to review")
                console.print()

                edit_choice = console.input("[yellow]Select:[/yellow] ").strip()

                if edit_choice == '1':
                    new_xp = console.input("[yellow]New XP reward:[/yellow] ").strip()
                    if new_xp.isdigit():
                        quest_data['xp_reward'] = int(new_xp)
                        console.print(f"  [green]✓[/green] XP set to {quest_data['xp_reward']}")
                    else:
                        console.print("[red]Invalid XP value[/red]")
                elif edit_choice == '2':
                    console.print("[yellow]Category:[/yellow]")
                    console.print("  1. social")
                    console.print("  2. constitutional")
                    console.print("  3. creative")
                    console.print("  4. experiential")
                    cat_choice = console.input("[yellow]Select (1-4):[/yellow] ").strip()
                    cat_map = {"1": "social", "2": "constitutional", "3": "creative", "4": "experiential"}
                    if cat_choice in cat_map:
                        quest_data['category'] = cat_map[cat_choice]
                        console.print(f"  [green]✓[/green] Category set to {quest_data['category']}")
                    else:
                        console.print("[red]Invalid choice[/red]")
                elif edit_choice == '3':
                    new_title = console.input("[yellow]New title:[/yellow] ").strip()
                    if new_title:
                        quest_data['title'] = new_title
                        console.print(f"  [green]✓[/green] Title set to {quest_data['title']}")

                # Show updated quest
                console.print()
                console.print("[cyan bold]Updated Quest:[/cyan bold]")
                console.print(f"  Title: {quest_data['title']}")
                console.print(f"  Category: {quest_data['category']}")
                console.print(f"  XP Reward: {quest_data['xp_reward']}")
                if quest_data.get('renewal_type'):
                    console.print(f"  Renewal: {quest_data['renewal_type']}")
                console.print()

            elif confirm == 'y':
                break

        # Convert renewal_type to RenewalPolicy
        renewal_policy = None
        if renewal_type:
            from src.domain.quests import RenewalPolicy
            cooldown_map = {
                "daily": 1,
                "weekly": 7,
                "monthly": 30,
                "seasonal": 90
            }
            cooldown_days = cooldown_map.get(renewal_type, 7)
            renewal_policy = RenewalPolicy(renewal_type=renewal_type, cooldown_days=cooldown_days)

        # Create quest
        quest = self.engine.create_quest(
            title=quest_data['title'],
            description=quest_data.get('description', ''),
            category=quest_data['category'],
            difficulty="easy" if quest_data['xp_reward'] <= 10 else "medium" if quest_data['xp_reward'] <= 20 else "hard",
            xp_reward=quest_data['xp_reward'],
            renewal_policy=renewal_policy,
            constraint_type=quest_data.get('constraint_type'),
            constraint_note=quest_data.get('constraint_note')
        )

        console.print()
        console.print(f"[green]✓ Quest created! [{quest.id}] {quest.title}[/green]")
        time.sleep(1.5)

    def _complete_quest(self, quests):
        """Complete a quest."""
        if not quests:
            console.print("[red]No active quests to complete[/red]")
            time.sleep(1)
            return

        console.print()
        quest_id = console.input("Quest ID to complete: ").strip()
        try:
            quest_id = int(quest_id)
        except ValueError:
            console.print("[red]Invalid ID[/red]")
            time.sleep(1)
            return

        # Complete quest
        try:
            result = self.engine.complete_quest(quest_id)

            console.print()
            console.print(f"[green bold]Quest completed! +{result.xp_awarded} XP[/green bold]")
            console.print(f"[dim]Total XP: {result.total_xp}[/dim]")
            console.print()
            console.print("[cyan]Mood buffs applied:[/cyan]")
            for event_type, modifier in result.mood_buffs_applied:
                console.print(f"  [green]{modifier:+d}[/green] {event_type}")
            time.sleep(2)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            time.sleep(1)

    def _snooze_quest(self, quests):
        """Snooze a quest."""
        if not quests:
            console.print("[red]No active quests to snooze[/red]")
            time.sleep(1)
            return

        console.print()
        quest_id = console.input("Quest ID to snooze: ").strip()
        try:
            quest_id = int(quest_id)
        except ValueError:
            console.print("[red]Invalid ID[/red]")
            time.sleep(1)
            return

        console.print()
        console.print("[cyan bold]Reason (optional):[/cyan bold]")
        console.print("  [cyan bold]1[/cyan bold]. Weather")
        console.print("  [cyan bold]2[/cyan bold]. Don't have time")
        console.print("  [cyan bold]3[/cyan bold]. Not in the mood")
        console.print("  [cyan bold]4[/cyan bold]. Other")
        console.print("  [dim][Enter to skip][/dim]")

        reason_choice = console.input("[yellow]Select reason (1-4, or Enter to skip):[/yellow] ").strip()
        reason_map = {
            "1": "weather",
            "2": "time",
            "3": "mood",
            "4": "custom"
        }

        reason = None
        if reason_choice in reason_map:
            reason = reason_map[reason_choice]
            if reason == "custom":
                reason = console.input("Custom reason: ").strip()

        self.engine.snooze_quest(quest_id, reason)
        console.print("[green]Quest snoozed[/green]")
        time.sleep(1)

    def _show_history(self):
        """Show completed quests."""
        console.clear()
        console.print()
        console.print(Align.center(Text("Quest History", style="cyan bold")))
        console.print()

        history = self.engine.get_quest_history()

        if not history:
            console.print("[dim]No completed quests yet[/dim]")
        else:
            for completion in history:
                # Get the quest details
                try:
                    quest = self.engine.get_quest_by_id(completion.quest_id)
                    console.print(f"[green]✓[/green] {quest.title} [{completion.xp_awarded} XP]")
                    console.print(f"    [dim]{quest.description}[/dim]")
                    if completion.notes:
                        console.print(f"    [dim italic]Note: {completion.notes}[/dim italic]")
                except ValueError:
                    # Quest was deleted or not found
                    console.print(f"[green]✓[/green] Quest #{completion.quest_id} [{completion.xp_awarded} XP]")
                console.print()

        console.print()
        console.input("[yellow]Press Enter to continue...[/yellow]")

    def _manage_quests(self, quests):
        """Quest management submenu."""
        while True:
            console.clear()
            console.print()
            console.print(Align.center(Text("Quest Management", style="cyan bold")))
            console.print()

            console.print("[yellow]Management Options:[/yellow]")
            console.print("  [cyan bold]d[/cyan bold] - Delete a quest")
            console.print("  [cyan bold]r[/cyan bold] - [red]Destroy ALL quest data[/red]")
            console.print("  [cyan bold]b[/cyan bold] - Back")
            console.print()

            choice = console.input("[yellow]Enter choice (d/r/b):[/yellow] ").strip().lower()

            if choice == 'b':
                break
            elif choice == 'd':
                self._delete_quest(quests)
            elif choice == 'r':
                self._destroy_all_quests()
                break  # Return to main menu after reset

    def _delete_quest(self, quests):
        """Delete a quest permanently."""
        if not quests:
            console.print("[red]No active quests to delete[/red]")
            time.sleep(1)
            return

        console.print()
        quest_id_input = console.input("[yellow]Enter quest ID to delete (or Enter to cancel):[/yellow] ").strip()

        if not quest_id_input:
            console.print("[dim]Cancelled[/dim]")
            time.sleep(1)
            return

        try:
            quest_id = int(quest_id_input)
            quest = self.engine.get_quest_by_id(quest_id)

            # Confirm deletion
            console.print()
            console.print(f"[red]Delete quest:[/red] {quest.title}")
            confirm = console.input("[yellow]Are you sure? (y/n):[/yellow] ").strip().lower()

            if confirm == 'y':
                # Remove from engine's internal state
                if quest_id in self.engine.quest_manager._quests:
                    del self.engine.quest_manager._quests[quest_id]

                # Delete from database
                with self.engine.db._get_connection() as conn:
                    conn.execute("DELETE FROM quests WHERE id = ?", (quest_id,))
                    conn.execute("DELETE FROM quest_completions WHERE quest_id = ?", (quest_id,))

                console.print("[green]✓ Quest deleted[/green]")
            else:
                console.print("[dim]Cancelled[/dim]")

        except (ValueError, KeyError):
            console.print("[red]Quest not found[/red]")

        time.sleep(1)

    def _destroy_all_quests(self):
        """Destroy ALL quest data while keeping user profile."""
        console.print()
        console.print("[red bold]⚠️  DESTROY ALL QUEST DATA ⚠️[/red bold]")
        console.print()
        console.print("[red]This will permanently delete:[/red]")
        console.print("  • All active quests")
        console.print("  • All quest completions")
        console.print("  • All XP earned")
        console.print()
        console.print("[green]Your profile settings will be preserved:[/green]")
        console.print("  • Location and zipcode")
        console.print("  • Memberships")
        console.print("  • Transportation preferences")
        console.print()

        confirm1 = console.input("[yellow]Type 'DESTROY' (all caps) to confirm:[/yellow] ").strip()

        if confirm1 != 'DESTROY':
            console.print("[dim]Cancelled[/dim]")
            time.sleep(1)
            return

        # Clear all quest data
        with self.engine.db._get_connection() as conn:
            conn.execute("DELETE FROM quests")
            conn.execute("DELETE FROM quest_completions")
            conn.execute("DELETE FROM quest_completion_modifiers")
            conn.execute("UPDATE user_stats SET total_xp = 0 WHERE id = 1")

        # Clear engine state
        self.engine.quest_manager._quests = {}
        self.engine._completions = []

        console.print()
        console.print("[green]✓ All quest data destroyed. Your profile has been preserved.[/green]")
        time.sleep(2)


class LogActionScreen:
    """Log mood-affecting events."""

    def __init__(self, engine):
        self.engine = engine

    def show(self):
        """Display mood logging interface."""
        console.clear()

        console.print()
        console.print(Align.center(Text("LogAction - Mood Events", style="cyan bold")))
        console.print()

        # Show quick options from library
        stock_modifiers = self.engine.get_mood_modifier_library()[:8]

        console.print("[cyan bold]Quick Options:[/cyan bold]")
        for i, modifier in enumerate(stock_modifiers, 1):
            mod_style = "green" if modifier.default_value >= 0 else "red"
            console.print(f"  [cyan bold]{i}[/cyan bold]. [{mod_style}]{modifier.default_value:+d}[/{mod_style}] {modifier.name}")
        console.print(f"  [cyan bold]9[/cyan bold]. Custom event")
        console.print(f"  [cyan bold]0[/cyan bold]. Cancel")
        console.print()

        choice = console.input("[yellow]Enter choice (1-9, or 0 to cancel):[/yellow] ").strip()

        if choice == '0':
            return

        if choice == '9':
            # Custom event
            desc = console.input("Event description: ").strip()
            if not desc:
                return

            modifier_str = console.input("Mood modifier (e.g., +5 or -3): ").strip()
            try:
                modifier_val = int(modifier_str)
            except ValueError:
                console.print("[red]Invalid modifier[/red]")
                time.sleep(1)
                return

            self.engine.log_mood_event("custom", modifier_val, desc)
            console.print(f"[green]Logged: {desc} ({modifier_val:+d})[/green]")
        else:
            try:
                idx = int(choice) - 1
                if idx < 0 or idx >= len(stock_modifiers):
                    raise IndexError

                modifier = stock_modifiers[idx]
                self.engine.log_mood_event(
                    modifier.event_type,
                    modifier.default_value,
                    modifier.name,
                    modifier.duration_hours
                )
                console.print(f"[green]Logged: {modifier.name} ({modifier.default_value:+d})[/green]")
            except (ValueError, IndexError):
                console.print("[red]Invalid choice[/red]")

        time.sleep(1.5)


class AboutScreen:
    """About MOOdBBS."""

    def show(self):
        """Display about information."""
        console.clear()

        console.print()
        console.print(Align.center(Text("About MOOdBBS", style="cyan bold")))
        console.print()

        about_text = """
MOOdBBS v0.1.0

A RimWorld-inspired mood tracking system with quest mechanics
and a nostalgic 90s BBS aesthetic.

Your real world as an ARG (Alternate Reality Game).

Built with Python + Rich
Headless architecture for multiple frontends

Created by nthmost
        """

        console.print(Align.center(about_text.strip(), style="dim"))
        console.print()
        console.input("[yellow]Press Enter to return...[/yellow]")


class SettingsScreen:
    """Settings and configuration."""

    def __init__(self, engine):
        self.engine = engine

    def show(self):
        """Display settings menu."""
        while True:
            console.clear()
            console.print()
            console.print(Align.center(Text("Settings", style="cyan bold")))
            console.print()

            # Get current profile
            profile = self.engine.db.get_user_profile()

            # Display current settings
            console.print("[cyan bold]Current Profile:[/cyan bold]")
            if profile.home_zipcode:
                console.print(f"  Zipcode: {profile.home_zipcode}")
            else:
                console.print("  Zipcode: [dim]not set[/dim]")

            transport = []
            if profile.prefers_walking:
                transport.append("walking")
            if profile.prefers_biking:
                transport.append("biking")
            if profile.prefers_transit:
                transport.append("transit")
            if profile.has_car:
                transport.append("car")
            if transport:
                console.print(f"  Transportation: {', '.join(transport)}")
            else:
                console.print("  Transportation: [dim]none set[/dim]")

            if profile.memberships:
                console.print(f"  Memberships: {', '.join(profile.memberships)}")
            else:
                console.print("  Memberships: [dim]none[/dim]")

            console.print()

            # Options
            console.print("[yellow]Settings Options:[/yellow]")
            console.print("  [cyan bold]z[/cyan bold] - Change zipcode")
            console.print("  [cyan bold]t[/cyan bold] - Update transportation preferences")
            console.print("  [cyan bold]m[/cyan bold] - Manage memberships")
            console.print("  [cyan bold]b[/cyan bold] - Back to menu")
            console.print()

            choice = console.input("[yellow]Enter choice (z/t/m/b):[/yellow] ").strip().lower()

            if choice == 'b':
                break
            elif choice == 'z':
                self._update_zipcode(profile)
            elif choice == 't':
                self._update_transportation(profile)
            elif choice == 'm':
                self._update_memberships(profile)

    def _update_zipcode(self, profile):
        """Update user's zipcode."""
        console.print()
        console.print(f"[dim]Current: {profile.home_zipcode or 'not set'}[/dim]")
        console.print("[dim]Examples: 94118 or 94118-1234 (US), A1A 1A1 (CA), SW1A 1AA (UK)[/dim]")

        while True:
            new_zipcode = console.input("[yellow]New zipcode (or Enter to keep current):[/yellow] ").strip()

            if not new_zipcode:
                console.print("[dim]No change[/dim]")
                time.sleep(1)
                return

            # Validate zipcode
            is_valid, error_msg = zipcode_validator.validate(new_zipcode)

            if is_valid:
                # Normalize the zipcode
                normalized = zipcode_validator.normalize(new_zipcode)
                profile.home_zipcode = normalized
                self.engine.db.save_user_profile(profile)
                console.print(f"[green]✓ Zipcode updated to {normalized}[/green]")
                time.sleep(1)
                return
            else:
                console.print(f"[red]✗ {error_msg}[/red]")
                console.print("[dim]Try again or press Enter to cancel[/dim]")

    def _update_transportation(self, profile):
        """Update transportation preferences."""
        console.print()
        console.print("[yellow]Select transportation modes (select all that apply):[/yellow]")
        console.print()
        console.print("  [cyan bold]w[/cyan bold] - Walking")
        console.print("  [cyan bold]b[/cyan bold] - Biking")
        console.print("  [cyan bold]t[/cyan bold] - Public transit")
        console.print("  [cyan bold]c[/cyan bold] - Car")
        console.print("  [cyan bold]a[/cyan bold] - All of the above")
        console.print("  [cyan bold]d[/cyan bold] - Done selecting")
        console.print()

        transport_prefs = []
        while True:
            choice = console.input("[yellow]Select:[/yellow] ").strip().lower()

            if choice == 'a':
                transport_prefs = ['walking', 'biking', 'transit', 'car']
                console.print("  [green]✓[/green] Selected all transportation modes")
                break
            elif choice == 'w' and 'walking' not in transport_prefs:
                transport_prefs.append('walking')
                console.print("  [green]✓[/green] Added walking")
            elif choice == 'b' and 'biking' not in transport_prefs:
                transport_prefs.append('biking')
                console.print("  [green]✓[/green] Added biking")
            elif choice == 't' and 'transit' not in transport_prefs:
                transport_prefs.append('transit')
                console.print("  [green]✓[/green] Added transit")
            elif choice == 'c' and 'car' not in transport_prefs:
                transport_prefs.append('car')
                console.print("  [green]✓[/green] Added car")
            elif choice == 'd':
                break

        profile.prefers_walking = 'walking' in transport_prefs
        profile.prefers_biking = 'biking' in transport_prefs
        profile.prefers_transit = 'transit' in transport_prefs
        profile.has_car = 'car' in transport_prefs

        if not transport_prefs:
            console.print("[dim]No preferences set, defaulting to walking[/dim]")
            profile.prefers_walking = True

        self.engine.db.save_user_profile(profile)
        console.print("[green]✓ Transportation preferences updated[/green]")
        time.sleep(1)

    def _update_memberships(self, profile):
        """Update user memberships."""
        console.print()
        if profile.memberships:
            console.print(f"[dim]Current: {', '.join(profile.memberships)}[/dim]")
        else:
            console.print("[dim]Current: none[/dim]")
        console.print()
        console.print("Enter memberships (comma-separated), or press Enter to keep current:")
        console.print("[dim]Examples: Cal Academy, SFMOMA, de Young, Exploratorium[/dim]")
        console.print("[dim]Leave blank to remove all memberships[/dim]")
        console.print()

        memberships_input = console.input("[yellow]Memberships:[/yellow] ").strip()

        if memberships_input == "":
            # User pressed Enter - ask if they want to keep current or clear
            console.print()
            console.print("[yellow]Keep current memberships or clear all?[/yellow]")
            console.print("  [cyan bold]k[/cyan bold] - Keep current")
            console.print("  [cyan bold]c[/cyan bold] - Clear all")
            keep_or_clear = console.input("[yellow]Select (k/c):[/yellow] ").strip().lower()

            if keep_or_clear == 'c':
                profile.memberships = []
                self.engine.db.save_user_profile(profile)
                console.print("[green]✓ All memberships cleared[/green]")
            else:
                console.print("[dim]No change[/dim]")
        else:
            profile.memberships = [m.strip() for m in memberships_input.split(',')]
            self.engine.db.save_user_profile(profile)
            console.print(f"[green]✓ Memberships updated ({len(profile.memberships)} total)[/green]")

        time.sleep(1)


class SetupWizardScreen:
    """First-run setup wizard to collect user profile information."""

    def __init__(self, engine):
        self.engine = engine

    def show(self):
        """Run the setup wizard."""
        console.clear()

        # Welcome message
        console.print()
        console.print(Align.center(Text("Welcome to MOOdBBS!", style="cyan bold")))
        console.print()
        console.print(Align.center("[yellow]Let's get you set up. This will only take a minute.[/yellow]"))
        console.print()
        time.sleep(1)

        # Get user profile
        profile = self.engine.db.get_user_profile()

        # Step 1: Zipcode
        console.clear()
        console.print()
        console.print(Align.center(Text("Setup: Location", style="cyan bold")))
        console.print()
        console.print("[yellow]What's your zipcode?[/yellow]")
        console.print("[dim]This helps us suggest relevant quests in your area.[/dim]")
        console.print("[dim]Examples: 94118 or 94118-1234 (US), A1A 1A1 (CA), SW1A 1AA (UK)[/dim]")
        console.print()

        while True:
            zipcode = console.input("[yellow]Zipcode (or Enter to skip):[/yellow] ").strip()

            if not zipcode:
                console.print("[dim]Skipped[/dim]")
                break

            # Validate zipcode
            is_valid, error_msg = zipcode_validator.validate(zipcode)

            if is_valid:
                # Normalize the zipcode
                normalized = zipcode_validator.normalize(zipcode)
                profile.home_zipcode = normalized
                console.print(f"[green]✓[/green] Set to {normalized}")
                break
            else:
                console.print(f"[red]✗ {error_msg}[/red]")
                console.print("[dim]Try again or press Enter to skip[/dim]")

        time.sleep(0.5)

        # Step 2: Transportation
        console.clear()
        console.print()
        console.print(Align.center(Text("Setup: Transportation", style="cyan bold")))
        console.print()
        console.print("[yellow]How do you usually get around? (select all that apply)[/yellow]")
        console.print()
        console.print("  [cyan bold]w[/cyan bold] - Walking")
        console.print("  [cyan bold]b[/cyan bold] - Biking")
        console.print("  [cyan bold]t[/cyan bold] - Public transit")
        console.print("  [cyan bold]c[/cyan bold] - Car")
        console.print("  [cyan bold]a[/cyan bold] - All of the above")
        console.print("  [cyan bold]d[/cyan bold] - Done selecting")
        console.print()

        transport_prefs = []
        while True:
            choice = console.input("[yellow]Select:[/yellow] ").strip().lower()

            if choice == 'a':
                transport_prefs = ['walking', 'biking', 'transit', 'car']
                console.print("  [green]✓[/green] Selected all transportation modes")
                break
            elif choice == 'w' and 'walking' not in transport_prefs:
                transport_prefs.append('walking')
                console.print("  [green]✓[/green] Added walking")
            elif choice == 'b' and 'biking' not in transport_prefs:
                transport_prefs.append('biking')
                console.print("  [green]✓[/green] Added biking")
            elif choice == 't' and 'transit' not in transport_prefs:
                transport_prefs.append('transit')
                console.print("  [green]✓[/green] Added transit")
            elif choice == 'c' and 'car' not in transport_prefs:
                transport_prefs.append('car')
                console.print("  [green]✓[/green] Added car")
            elif choice == 'd':
                break

        profile.prefers_walking = 'walking' in transport_prefs
        profile.prefers_biking = 'biking' in transport_prefs
        profile.prefers_transit = 'transit' in transport_prefs
        profile.has_car = 'car' in transport_prefs

        if not transport_prefs:
            console.print("[dim]No preferences set, defaulting to walking[/dim]")
            profile.prefers_walking = True

        time.sleep(0.5)

        # Step 3: Memberships
        console.clear()
        console.print()
        console.print(Align.center(Text("Setup: Memberships", style="cyan bold")))
        console.print()
        console.print("[yellow]Do you have any museum or venue memberships?[/yellow]")
        console.print("[dim]We'll suggest these as easy weekday quests since there's no admission cost.[/dim]")
        console.print("[dim]Plus, we'll learn what kinds of places you're interested in![/dim]")
        console.print()
        console.print("Enter memberships (comma-separated), or press Enter to skip:")
        console.print("[dim]Examples: Cal Academy, SFMOMA, de Young, Exploratorium[/dim]")
        console.print()
        memberships_input = console.input("[yellow]Memberships:[/yellow] ").strip()

        if memberships_input:
            profile.memberships = [m.strip() for m in memberships_input.split(',')]
            console.print(f"[green]✓[/green] Added {len(profile.memberships)} membership(s)")
        else:
            console.print("[dim]Skipped[/dim]")

        time.sleep(0.5)

        # Step 4: Confirmation
        console.clear()
        console.print()
        console.print(Align.center(Text("Setup Complete!", style="green bold")))
        console.print()
        console.print("[cyan]Your profile:[/cyan]")
        if profile.home_zipcode:
            console.print(f"  Location: {profile.home_zipcode}")
        transport = []
        if profile.prefers_walking:
            transport.append("walking")
        if profile.prefers_biking:
            transport.append("biking")
        if profile.prefers_transit:
            transport.append("transit")
        if profile.has_car:
            transport.append("car")
        if transport:
            console.print(f"  Transportation: {', '.join(transport)}")
        if profile.memberships:
            console.print(f"  Memberships: {', '.join(profile.memberships)}")
        console.print()
        console.print("[dim]You can update these settings anytime from the Settings menu.[/dim]")
        console.print()

        # Mark setup as completed
        profile.setup_completed = True
        self.engine.db.save_user_profile(profile)

        console.input("[yellow]Press Enter to continue...[/yellow]")
        console.print()
        console.print(Align.center("[green]Let's start your MOOdBBS adventure![/green]"))
        time.sleep(1)
