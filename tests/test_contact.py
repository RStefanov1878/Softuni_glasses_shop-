"""Module B tests — contact logic (contact.py)."""

from datetime import datetime, timezone

import pytest

import contact

GOOD = {
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "message": "I would like to order the Aviator Classic, please.",
}
FIXED_NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


# --- validate ---------------------------------------------------------------

def test_validate_accepts_good_input():
    ok, errors = contact.validate(GOOD)
    assert ok is True
    assert errors == {}


def test_validate_flags_all_missing_fields():
    ok, errors = contact.validate({})
    assert ok is False
    assert set(errors) == {"name", "email", "message"}


def test_validate_rejects_bad_email():
    ok, errors = contact.validate({**GOOD, "email": "not-an-email"})
    assert ok is False
    assert "email" in errors
    assert "name" not in errors and "message" not in errors


def test_validate_rejects_short_message():
    ok, errors = contact.validate({**GOOD, "message": "hi"})
    assert ok is False
    assert "message" in errors


def test_validate_treats_whitespace_as_empty():
    ok, errors = contact.validate({"name": "   ", "email": "  ", "message": "   "})
    assert ok is False
    assert set(errors) == {"name", "email", "message"}


# --- persistence ------------------------------------------------------------

def test_load_missing_file_returns_empty(tmp_path):
    assert contact.load_messages(tmp_path / "messages.json") == []


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "messages.json"
    record = contact.save_message(GOOD, path, now=FIXED_NOW)

    assert record["received_at"] == FIXED_NOW.isoformat()
    loaded = contact.load_messages(path)
    assert len(loaded) == 1
    assert loaded[0]["name"] == "Ada Lovelace"
    assert loaded[0]["received_at"] == FIXED_NOW.isoformat()


def test_save_appends_and_preserves_order(tmp_path):
    path = tmp_path / "messages.json"
    contact.save_message({**GOOD, "name": "First"}, path, now=FIXED_NOW)
    contact.save_message({**GOOD, "name": "Second"}, path, now=FIXED_NOW)

    names = [m["name"] for m in contact.load_messages(path)]
    assert names == ["First", "Second"]


def test_save_creates_missing_parent_dir(tmp_path):
    path = tmp_path / "nested" / "dir" / "messages.json"
    contact.save_message(GOOD, path, now=FIXED_NOW)
    assert path.exists()
    assert len(contact.load_messages(path)) == 1


def test_load_rejects_non_list(tmp_path):
    path = tmp_path / "messages.json"
    path.write_text('{"not": "a list"}', encoding="utf-8")
    with pytest.raises(ValueError):
        contact.load_messages(path)
