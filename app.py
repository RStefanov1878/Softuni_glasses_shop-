"""Module C — Web app / routes.

Flask application wiring the data layer (Module A) and contact logic
(Module B) to Jinja templates.

Routes:
    GET       /                  catalogue grid (optional ?category= filter)
    GET       /glasses/<id>      detail page for one pair of glasses
    GET/POST  /contact           contact form (POST validates + saves)
    404                          friendly not-found page

The catalogue is loaded once at start-up (it never changes at runtime).
Contact submissions are appended to data/messages.json.
"""

from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for

import catalogue
import contact

BASE_DIR = Path(__file__).resolve().parent
GLASSES_PATH = BASE_DIR / "data" / "glasses.json"
MESSAGES_PATH = BASE_DIR / "data" / "messages.json"

app = Flask(__name__)

# Loaded once — the catalogue is static data, not a live database.
GLASSES = catalogue.load_glasses(GLASSES_PATH)


@app.route("/")
def index():
    """Catalogue grid, optionally filtered by ?category=."""
    selected = request.args.get("category")
    if selected:
        glasses = catalogue.filter_by_category(GLASSES, selected)
    else:
        glasses = catalogue.get_all(GLASSES)
    return render_template(
        "index.html",
        glasses=glasses,
        categories=catalogue.categories(GLASSES),
        selected=selected,
    )


@app.route("/glasses/<int:glasses_id>")
def detail(glasses_id):
    """Detail page for a single pair of glasses (404 if the id is unknown)."""
    item = catalogue.get_by_id(GLASSES, glasses_id)
    if item is None:
        abort(404)
    return render_template("detail.html", g=item)


@app.route("/contact", methods=["GET", "POST"])
def contact_view():
    """Contact form. GET shows the form; POST validates then saves the message.

    On success we redirect to /contact?sent=1 (Post/Redirect/Get) so a browser
    refresh does not re-submit. On failure we re-render the form with the
    submitted values and per-field errors.
    """
    if request.method == "POST":
        ok, errors = contact.validate(request.form)
        if ok:
            contact.save_message(
                {
                    "name": request.form["name"].strip(),
                    "email": request.form["email"].strip(),
                    "message": request.form["message"].strip(),
                },
                MESSAGES_PATH,
            )
            return redirect(url_for("contact_view", sent=1))
        return render_template("contact.html", errors=errors, form=request.form, sent=False)

    sent = request.args.get("sent") == "1"
    return render_template("contact.html", errors={}, form={}, sent=sent)


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
