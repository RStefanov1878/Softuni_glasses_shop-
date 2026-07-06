"""Module A tests — data layer (catalogue.py)."""

import json
from pathlib import Path

import pytest

import catalogue

ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PATH = ROOT / "data" / "glasses.json"

# A tiny, self-contained fixture used by the query tests (independent of the
# real committed dataset so these tests never break when the catalogue grows).
SAMPLE = [
    {"id": 1, "name": "Aviator Classic", "category": "sunglasses", "price": 89.99},
    {"id": 2, "name": "Retro Round", "category": "sunglasses", "price": 69.0},
    {"id": 3, "name": "Reader Slim", "category": "reading", "price": 39.99},
]


# --- load_glasses -----------------------------------------------------------

def test_load_glasses_reads_file(tmp_path):
    path = tmp_path / "g.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    assert catalogue.load_glasses(path) == SAMPLE


def test_load_glasses_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        catalogue.load_glasses(tmp_path / "nope.json")


def test_load_glasses_rejects_non_list(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"not": "a list"}', encoding="utf-8")
    with pytest.raises(ValueError):
        catalogue.load_glasses(path)


def test_committed_sample_is_valid():
    """The real dataset shipped in the repo must be well-formed."""
    items = catalogue.load_glasses(SAMPLE_PATH)
    assert len(items) >= 3
    required = {"id", "name", "category", "price"}
    for item in items:
        assert required <= item.keys()
    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids)), "ids must be unique"


# --- query helpers ----------------------------------------------------------

def test_get_all_returns_everything():
    assert catalogue.get_all(SAMPLE) == SAMPLE


def test_get_all_returns_a_copy():
    result = catalogue.get_all(SAMPLE)
    result.clear()
    assert len(SAMPLE) == 3  # original list is untouched


def test_get_by_id_hit():
    assert catalogue.get_by_id(SAMPLE, 2)["name"] == "Retro Round"


def test_get_by_id_miss_returns_none():
    assert catalogue.get_by_id(SAMPLE, 999) is None


def test_filter_by_category():
    suns = catalogue.filter_by_category(SAMPLE, "sunglasses")
    assert [g["id"] for g in suns] == [1, 2]


def test_filter_by_unknown_category_is_empty():
    assert catalogue.filter_by_category(SAMPLE, "monocle") == []


def test_categories_are_sorted_and_unique():
    assert catalogue.categories(SAMPLE) == ["reading", "sunglasses"]
