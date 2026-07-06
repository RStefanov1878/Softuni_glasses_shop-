"""Module A — Data layer.

Loads and queries the glasses catalogue from a JSON file. These are pure
functions that operate on an in-memory list of glasses (each a dict), which
keeps them trivial to unit-test with a small fixture and free of global state.

The Flask app (Module C) loads the catalogue once at start-up with
``load_glasses()`` and passes the resulting list to the query helpers below.
"""

import json


def load_glasses(path):
    """Read the catalogue JSON file at *path* and return a list of glasses.

    Raises ``FileNotFoundError`` if the file is missing and ``ValueError`` if
    the JSON root is not a list (a corrupt/unexpected catalogue file).
    """
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError(
            f"Expected a JSON list of glasses, got {type(data).__name__}"
        )
    return data


def get_all(glasses):
    """Return all glasses as a new list (a defensive copy of the input)."""
    return list(glasses)


def get_by_id(glasses, glasses_id):
    """Return the single pair of glasses whose ``id`` matches, else ``None``."""
    for item in glasses:
        if item.get("id") == glasses_id:
            return item
    return None


def filter_by_category(glasses, category):
    """Return only the glasses whose ``category`` matches exactly."""
    return [item for item in glasses if item.get("category") == category]


def categories(glasses):
    """Return the sorted, unique list of categories present in the catalogue."""
    return sorted({item["category"] for item in glasses if item.get("category")})
