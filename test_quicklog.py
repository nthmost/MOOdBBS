#!/usr/bin/env python3
"""Test script for QuickLog interface."""

import sys
from src.engine import MOOdBBSEngine
from rich.console import Console

console = Console()

def test_quicklog_categories():
    """Test that QuickLog can load and display all categories."""
    engine = MOOdBBSEngine()

    # Get all event moodlets
    all_moodlets = engine.get_all_event_moodlets()

    # Group by category
    by_category = {}
    for m in all_moodlets:
        cat = m['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(m)

    console.print("\n[cyan bold]QuickLog Categories Test[/cyan bold]\n")

    for i, (category, moodlets) in enumerate(sorted(by_category.items()), 1):
        console.print(f"[yellow]{i}.[/yellow] [cyan]{category.title()}[/cyan] ({len(moodlets)} moodlets)")

        # Show a few example moodlets from each category
        for j, m in enumerate(moodlets[:3], 1):
            mood_val = m['mood_value']
            mod_style = "green" if mood_val > 0 else "red" if mood_val < 0 else "dim"

            backoff_info = ""
            if m.get('backoff_value') and m.get('backoff_duration_hours'):
                backoff_info = f" → [{mod_style}]{m['backoff_value']:+d}[/{mod_style}] for {m['backoff_duration_hours']}h"

            console.print(
                f"   {j}. [{mod_style}]{mood_val:+d}[/{mod_style}] {m['name']} "
                f"({m['duration_hours']}h{backoff_info})"
            )

        if len(moodlets) > 3:
            console.print(f"   ... and {len(moodlets) - 3} more")
        console.print()

    console.print(f"[green]✓[/green] Total categories: {len(by_category)}")
    console.print(f"[green]✓[/green] Total event moodlets: {len(all_moodlets)}\n")

    return len(by_category) > 0 and len(all_moodlets) > 0


def test_apply_moodlet():
    """Test applying a moodlet and checking it appears in mood stats."""
    engine = MOOdBBSEngine()

    console.print("[cyan bold]Testing Moodlet Application[/cyan bold]\n")

    # Get baseline mood
    mood_before = engine.get_current_mood()
    console.print(f"Mood before: {mood_before.score} {mood_before.face}")

    # Apply "Gave someone a compliment" (ID 95, +2 for 2h)
    console.print("\nApplying: 'Gave someone a compliment' (+2, 2h)...")
    engine.apply_moodlet(95)

    # Get new mood
    mood_after = engine.get_current_mood()
    console.print(f"Mood after: {mood_after.score} {mood_after.face}")

    # Verify it increased
    expected_increase = 2
    actual_increase = mood_after.score - mood_before.score

    if actual_increase == expected_increase:
        console.print(f"[green]✓[/green] Mood increased by {expected_increase} as expected\n")
        return True
    else:
        console.print(f"[red]✗[/red] Expected +{expected_increase}, got +{actual_increase}\n")
        return False


def test_negative_moodlet():
    """Test applying a negative moodlet."""
    engine = MOOdBBSEngine()

    console.print("[cyan bold]Testing Negative Moodlet[/cyan bold]\n")

    # Get baseline mood
    mood_before = engine.get_current_mood()
    console.print(f"Mood before: {mood_before.score} {mood_before.face}")

    # Apply "Flirted (unwelcome)" (ID 104, -5 for 2h)
    console.print("\nApplying: 'Flirted (unwelcome)' (-5, 2h)...")
    engine.apply_moodlet(104)

    # Get new mood
    mood_after = engine.get_current_mood()
    console.print(f"Mood after: {mood_after.score} {mood_after.face}")

    # Verify it decreased
    expected_decrease = -5
    actual_change = mood_after.score - mood_before.score

    if actual_change == expected_decrease:
        console.print(f"[green]✓[/green] Mood decreased by 5 as expected\n")
        return True
    else:
        console.print(f"[red]✗[/red] Expected {expected_decrease}, got {actual_change}\n")
        return False


def main():
    """Run all tests."""
    console.print("\n" + "="*60)
    console.print("[cyan bold]MOOdBBS QuickLog Test Suite[/cyan bold]")
    console.print("="*60 + "\n")

    tests = [
        ("Category Loading", test_quicklog_categories),
        ("Positive Moodlet Application", test_apply_moodlet),
        ("Negative Moodlet Application", test_negative_moodlet),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            console.print(f"[red]Error in {name}: {e}[/red]\n")
            results.append((name, False))

    # Summary
    console.print("="*60)
    console.print("[cyan bold]Test Summary[/cyan bold]")
    console.print("="*60 + "\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[green]PASS[/green]" if result else "[red]FAIL[/red]"
        console.print(f"{status} - {name}")

    console.print(f"\n{passed}/{total} tests passed\n")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
