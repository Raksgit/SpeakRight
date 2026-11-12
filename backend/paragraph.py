"""Paragraph dataset loader for SpeakRight.

Reads practice paragraphs from data/paragraphs.json and returns a random
one for the requested difficulty level.
"""

from __future__ import annotations

import json
import random
from functools import cache
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_FILE = BASE_DIR / "data" / "paragraphs.json"


# ---------------------------------------------------------------------------
# Dataset loading and validation
# ---------------------------------------------------------------------------
@cache
def load_paragraphs(path: Path = DATASET_FILE) -> dict[str, list[str]]:
    """Load and validate the paragraph dataset.

    The result is cached, so the file is read only once per run.
    Restart the program after editing the JSON file.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Paragraph dataset not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    _validate(data)
    return data


def _validate(data: object) -> None:
    """Make sure the dataset has the structure the app expects."""
    if not isinstance(data, dict) or not data:
        raise ValueError("Dataset must be a non-empty JSON object keyed by level.")

    for level, paragraphs in data.items():
        if level != level.lower():
            raise ValueError(f"Level key '{level}' must be lowercase.")

        is_valid_list = (
            isinstance(paragraphs, list)
            and len(paragraphs) > 0
            and all(isinstance(p, str) and p.strip() for p in paragraphs)
        )
        if not is_valid_list:
            raise ValueError(
                f"Level '{level}' must be a non-empty list of text paragraphs."
            )


# ---------------------------------------------------------------------------
# Public API (used by the CLI now, and by FastAPI later)
# ---------------------------------------------------------------------------
def get_levels() -> list[str]:
    """Return the available difficulty levels, e.g. ['easy', 'medium', 'hard']."""
    return list(load_paragraphs())


def get_random_paragraph(level: str) -> str:
    """Return a random paragraph for the given level (case-insensitive)."""
    paragraphs = load_paragraphs()
    key = level.strip().lower()

    if key not in paragraphs:
        raise ValueError(
            f"Invalid level: '{level}'. Choose from: {', '.join(paragraphs)}."
        )

    return random.choice(paragraphs[key])


# ---------------------------------------------------------------------------
# Command-line test
# ---------------------------------------------------------------------------
def main() -> None:
    options = ", ".join(level.title() for level in get_levels())
    level = input(f"Choose difficulty ({options}): ")

    try:
        paragraph = get_random_paragraph(level)
    except (ValueError, FileNotFoundError) as error:
        print(error)
        return

    print("\nYour practice paragraph:\n")
    print(paragraph)


if __name__ == "__main__":
    main()