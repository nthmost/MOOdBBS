"""Main menu UI for MOOdBBS."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.align import Align


def render_main_menu(console: Console):
    """Render the MOOdBBS main menu.

    Args:
        console: Rich Console instance
    """
    menu_text = """
====================================================
                    MOOdBBS MAIN
====================================================
   1) WanderMOO     - Explore today's quests
   2) MoodStats     - View buffs / debuffs / traits
   3) LogAction     - Manual entry using keyboard
   4) Settings      - Personalization details
   5) About         - i made this with my own hooves
====================================================
         Press a number on your numpad to begin
====================================================
"""

    console.print(menu_text, style="cyan")


def render_dashboard(console: Console, mood_score: int, mood_face: str, quests: list, active_events: list):
    """Render the main dashboard view.

    Args:
        console: Rich Console instance
        mood_score: Current mood score
        mood_face: ASCII mood face
        quests: List of active quests
        active_events: List of active mood events
    """
    console.clear()

    # Header
    header = Text("MOOdBBS", style="bold cyan", justify="center")
    console.print(Panel(header, border_style="cyan"))
    console.print()

    # Mood display
    mood_color = "green" if mood_score >= 10 else "yellow" if mood_score >= 0 else "red"
    mood_text = Text()
    mood_text.append(f"Mood: {mood_face} ", style=f"bold {mood_color}")
    mood_text.append(f"[{mood_score:+d}]", style=mood_color)

    console.print(Panel(mood_text, title="[bold]Current Mood[/bold]", border_style=mood_color))
    console.print()

    # Active quests
    if quests:
        quest_text = Text()
        for i, quest in enumerate(quests[:3], 1):
            quest_text.append(f"{i}. {quest['title']}\n", style="bold yellow")
            if quest.get('description'):
                quest_text.append(f"   {quest['description']}\n", style="white")
            quest_text.append(f"   XP: {quest['xp_reward']}", style="green")
            if i < len(quests):
                quest_text.append("\n\n")

        console.print(Panel(quest_text, title="[bold]Active Quests[/bold]", border_style="yellow"))
    else:
        console.print(Panel("No active quests", title="[bold]Active Quests[/bold]", border_style="yellow"))

    console.print()

    # Recent mood events
    if active_events:
        events_text = Text()
        for event in active_events[:5]:
            modifier_color = "green" if event['modifier'] > 0 else "red" if event['modifier'] < 0 else "white"
            events_text.append(f"{event['modifier']:+d} ", style=modifier_color)
            events_text.append(f"{event['event_type']}", style="white")
            if event.get('description'):
                events_text.append(f" - {event['description']}", style="dim")
            events_text.append("\n")

        console.print(Panel(events_text, title="[bold]Recent Mood Events[/bold]", border_style="blue"))
    else:
        console.print(Panel("No recent events", title="[bold]Recent Mood Events[/bold]", border_style="blue"))

    console.print()
    console.print("[dim]Press 1-5 for menu options[/dim]")


def render_ascii_art():
    """Return MOOdBBS ASCII art for boot screen."""
    return r"""
 ___  ___  ________  ________  ________  ________  ________  ________
|\  \|\  \|\   __  \|\   __  \|\   ___ \|\   __  \|\   __  \|\   ____\
\ \  \\\  \ \  \|\  \ \  \|\  \ \  \_|\ \ \  \|\ /\ \  \|\ /\ \  \___|_
 \ \   __  \ \  \\\  \ \  \\\  \ \  \ \\ \ \   __  \ \   __  \ \_____  \
  \ \  \ \  \ \  \\\  \ \  \\\  \ \  \_\\ \ \  \|\  \ \  \|\  \|____|\  \
   \ \__\ \__\ \_______\ \_______\ \_______\ \_______\ \_______\____\_\  \
    \|__|\|__|\|_______|\|_______|\|_______|\|_______|\|_______|\_________\
                                                                \|_________|

            [ A RimWorld-Style Mood Tracker & Quest System ]
                   [ Press ENTER to continue ]
"""


def render_connection_screen(console: Console):
    """Render the connection/boot screen."""
    console.clear()

    art = render_ascii_art()
    console.print(art, style="bold cyan")
