"""Module D tests — frontend assets (CSS + product images) served correctly."""

import pytest

import app as webapp
import catalogue


@pytest.fixture
def client():
    webapp.app.config.update(TESTING=True)
    return webapp.app.test_client()


def test_stylesheet_is_served(client):
    resp = client.get("/static/style.css")
    assert resp.status_code == 200
    assert "text/css" in resp.headers["Content-Type"]
    body = resp.get_data(as_text=True)
    assert ".card" in body and ".grid" in body


def test_index_links_the_stylesheet(client):
    body = client.get("/").get_data(as_text=True)
    assert "style.css" in body


def test_every_catalogue_image_exists(client):
    """Guard against a data entry pointing at a missing image (broken picture)."""
    glasses = catalogue.load_glasses(webapp.GLASSES_PATH)
    for item in glasses:
        resp = client.get(f"/static/img/{item['image']}")
        assert resp.status_code == 200, f"missing image for {item['name']}: {item['image']}"
