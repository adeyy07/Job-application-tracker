import os
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from database import (
    create_table,
    add_application,
    get_applications,
    update_status,
    delete_application,
    get_statistics
)

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "local-development-key"
)

SITE_PASSWORD = os.environ.get("SITE_PASSWORD")

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        password = request.form.get("password", "")

        if password == SITE_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("home"))

        error = "Incorrect password."

    return render_template(
        "login.html",
        error=error
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    create_table()

    search = request.args.get("search", "").strip()
    selected_status = request.args.get("status", "").strip()

    applications = get_applications()

    if search:
        applications = [
            application
            for application in applications
            if search.lower() in application[1].lower()
            or search.lower() in application[2].lower()
        ]

    if selected_status:
        applications = [
            application
            for application in applications
            if application[4].lower() == selected_status.lower()
        ]

    total, status_counts = get_statistics()

    interviews = 0
    offers = 0
    rejections = 0

    for status_name, count in status_counts:
        status_name = status_name.lower()

        if status_name == "interview":
            interviews = count

        elif status_name == "offer":
            offers = count

        elif status_name == "rejected":
            rejections = count

    return render_template(
        "index.html",
        applications=applications,
        total=total,
        interviews=interviews,
        offers=offers,
        rejections=rejections,
        search=search,
        selected_status=selected_status
    )


@app.route("/add", methods=["POST"])
@login_required
def add():
    company = request.form["company"].strip()
    position = request.form["position"].strip()
    date_applied = request.form["date_applied"].strip()
    status = request.form["status"].strip()
    salary = request.form["salary"].strip()
    notes = request.form["notes"].strip()

    if not company or not position or not date_applied:
        return redirect(url_for("home"))

    valid_statuses = [
        "Applied",
        "Interview",
        "Offer",
        "Rejected"
    ]

    if status not in valid_statuses:
        status = "Applied"

    add_application(
        company,
        position,
        date_applied,
        status,
        salary,
        notes
    )

    return redirect(url_for("home"))


@app.route("/update/<int:application_id>", methods=["POST"])
@login_required
def update(application_id):
    new_status = request.form["status"].strip()

    valid_statuses = [
        "Applied",
        "Interview",
        "Offer",
        "Rejected"
    ]

    if new_status in valid_statuses:
        update_status(
            application_id,
            new_status
        )

    return redirect(url_for("home"))


@app.route("/delete/<int:application_id>", methods=["POST"])
@login_required
def delete(application_id):
    delete_application(application_id)

    return redirect(url_for("home"))


if __name__ == "__main__":
    create_table()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )