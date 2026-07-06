# Glasses Catalogue

A small **Flask** web application: a catalogue of glasses (sunglasses, reading,
blue-light) that visitors can browse as a grid, filter by category, and open in a
detail view — plus a contact form whose submissions are validated and saved to a
local JSON file. **No database:** the catalogue is read from a committed JSON file
and messages are stored on disk.

Built for the *AI-Assisted Development* exam as a genuine, tested, incrementally
built project (one module at a time, human-in-the-loop).

## Functional requirements

1. Home page lists all glasses as cards (image, name, category, price).
2. Filter the catalogue by category (sunglasses / reading / blue-light).
3. Detail page for a single pair of glasses, by id.
4. Contact form (name, email, message).
5. Server-side validation with clear per-field errors and a success confirmation.
6. Accepted submissions are appended to `data/messages.json` (no database).
7. Catalogue data is loaded from a committed sample JSON file.
8. Friendly 404 page for unknown product ids.

## Modules

| Module | File(s) | What it does |
|---|---|---|
| **A — Data layer** | `catalogue.py` | Loads and queries the catalogue from JSON: all items, by id, filter by category, list categories. |
| **B — Contact logic** | `contact.py` | Validates contact-form input and persists messages to `data/messages.json`. |
| **C — Web app / routes** | `app.py` | Flask routes wiring the data and contact modules to templates (catalogue, detail, contact, 404). |
| **D — Frontend** | `templates/`, `static/` | Jinja templates + hand-written CSS + placeholder product images. |

**Build order:** A → B → C → D.

## Requirements

- **Python 3.10+** (developed and tested on Python 3.13)
- Dependencies in [`requirements.txt`](requirements.txt): Flask, pytest

## Run from a clean clone

```bash
git clone <your-repo-url>
cd glasses-catalogue

# 1. Create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the tests (should report: 33 passed)
pytest -v

# 4a. Run the one-command demo (prints the catalogue as a table)
python demo.py

# 4b. Or start the web app, then open http://127.0.0.1:5000/
flask --app app run
```

## Sample run

`data/glasses.json` is the committed sample dataset (7 items). The demo prints it:

```
$ python demo.py
Glasses Catalogue - 7 items across 3 categories: blue-light, reading, sunglasses

ID  NAME               CATEGORY       PRICE  COLOUR
---------------------------------------------------
 1  Aviator Classic    sunglasses    $89.99  Gold / Green
 2  Wayfarer Bold      sunglasses    $79.50  Matte Black
 3  Retro Round        sunglasses    $69.00  Tortoise
 4  Reader Slim +1.5   reading       $39.99  Matte Black
 5  Reader Bold +2.0   reading       $44.99  Burgundy
 6  ScreenGuard Blue   blue-light    $54.99  Clear / Grey
 7  FocusPlus Blue     blue-light    $59.99  Navy
```

In the web app: `/` shows the grid, the filter pills narrow by category,
`/glasses/1` opens a detail page, and `/contact` accepts a message (valid input
shows a success banner; invalid input shows per-field errors).

## Tests

```bash
pytest -v
```

33 tests across four files: `test_catalogue.py` (data layer), `test_contact.py`
(validation + persistence), `test_app.py` (routes via Flask's test client),
`test_frontend.py` (CSS + every product image is served).

## Repository

- GitHub: _(link to be added)_
