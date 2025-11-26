"""Trait system for MOOdBBS."""

from dataclasses import dataclass


@dataclass
class Trait:
    """A personality trait (RimWorld-style)."""
    id: int
    trait_name: str
    description: str
    mood_modifier: int
    is_active: bool
    category: str  # rimworld_stock, custom
