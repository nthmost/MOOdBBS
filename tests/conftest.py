"""Pytest configuration and shared fixtures."""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timezone

# We'll import the engine once it's created
# from src.engine import MOOdBBSEngine


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    yield db_path

    # Cleanup
    Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def now():
    """Current timestamp for testing."""
    return datetime.now(timezone.utc)


@pytest.fixture
def engine(temp_db):
    """Create a fresh game engine for each test."""
    # Placeholder - will implement once engine exists
    # return MOOdBBSEngine(db_path=temp_db)
    pass
