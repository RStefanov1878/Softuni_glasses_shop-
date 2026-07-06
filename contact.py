"""Module B — Contact logic.

Validates a contact-form submission and persists accepted messages to a JSON
file (no database). Validation is a pure function returning per-field errors,
and persistence takes an injectable clock so the tests stay deterministic.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

# Pragmatic email check (not full RFC 5322): one @, no spaces, a dotted domain.
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_MESSAGE_LENGTH = 10


def validate(form):
    """Validate a contact-form submission.

    *form* is a mapping with keys ``name``, ``email`` and ``message`` (e.g.
    Flask's ``request.form``). Returns ``(ok, errors)`` where *ok* is a bool and
    *errors* maps each invalid field to a human-readable message.
    """
    errors = {}
    name = (form.get("name") or "").strip()
    email = (form.get("email") or "").strip()
    message = (form.get("message") or "").strip()

    if not name:
        errors["name"] = "Please enter your name."

    if not email:
        errors["email"] = "Please enter your email address."
    elif not EMAIL_RE.match(email):
        errors["email"] = "Please enter a valid email address."

    if not message:
        errors["message"] = "Please enter a message."
    elif len(message) < MIN_MESSAGE_LENGTH:
        errors["message"] = f"Message must be at least {MIN_MESSAGE_LENGTH} characters."

    return (not errors, errors)


def load_messages(path):
    """Return the list of stored messages, or ``[]`` if the file doesn't exist.

    Raises ``ValueError`` if the file exists but its JSON root is not a list.
    """
    path = Path(path)
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError(
            f"Expected a JSON list of messages, got {type(data).__name__}"
        )
    return data


def save_message(message, path, now=None):
    """Append *message* (a dict) to the JSON list at *path* and return the
    stored record.

    Stamps the record with a UTC ``received_at`` ISO timestamp (override via
    *now* for deterministic tests) and creates the file and its parent
    directory if they do not yet exist.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    record = dict(message)
    record["received_at"] = now.isoformat()

    path = Path(path)
    messages = load_messages(path)
    messages.append(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(messages, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return record
