"""Module C tests — Flask routes (app.py), via the test client."""

import pytest

import app as webapp
import contact


@pytest.fixture
def client():
    webapp.app.config.update(TESTING=True)
    return webapp.app.test_client()


# --- catalogue --------------------------------------------------------------

def test_index_lists_all_glasses(client):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Our Glasses" in body
    assert "Aviator Classic" in body
    assert "FocusPlus Blue" in body


def test_index_filter_by_category(client):
    resp = client.get("/?category=reading")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Reader Slim +1.5" in body
    assert "Aviator Classic" not in body  # a sunglasses item is filtered out


def test_index_unknown_category_is_empty(client):
    resp = client.get("/?category=monocle")
    assert resp.status_code == 200
    assert "No glasses found" in resp.get_data(as_text=True)


# --- detail -----------------------------------------------------------------

def test_detail_page_ok(client):
    resp = client.get("/glasses/1")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Aviator Classic" in body
    assert "Gold / Green" in body


def test_detail_missing_returns_404(client):
    resp = client.get("/glasses/999")
    assert resp.status_code == 404
    assert "404" in resp.get_data(as_text=True)


# --- contact ----------------------------------------------------------------

def test_contact_get_shows_form(client):
    resp = client.get("/contact")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert 'name="name"' in body
    assert 'name="email"' in body
    assert 'name="message"' in body


def test_contact_post_valid_saves_and_redirects(client, tmp_path, monkeypatch):
    msgs = tmp_path / "messages.json"
    monkeypatch.setattr(webapp, "MESSAGES_PATH", msgs)

    resp = client.post(
        "/contact",
        data={
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "message": "I would like the Aviator Classic please.",
        },
    )
    assert resp.status_code == 302
    assert "sent=1" in resp.headers["Location"]

    saved = contact.load_messages(msgs)
    assert len(saved) == 1
    assert saved[0]["name"] == "Ada Lovelace"


def test_contact_post_invalid_shows_errors(client, tmp_path, monkeypatch):
    msgs = tmp_path / "messages.json"
    monkeypatch.setattr(webapp, "MESSAGES_PATH", msgs)

    resp = client.post("/contact", data={"name": "", "email": "bad", "message": "hi"})
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "valid email" in body
    assert not msgs.exists()  # nothing was saved


def test_contact_sent_banner(client):
    resp = client.get("/contact?sent=1")
    assert resp.status_code == 200
    assert "has been sent" in resp.get_data(as_text=True)
