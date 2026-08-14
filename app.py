from flask import Flask, render_template, request, redirect, url_for
from database import (
    create_table,
    add_application,
    get_applications,
    update_status,
    delete_application,
    get_statistics
)

app = Flask(__name__)


@app.route("/")
def home():
    create_table()

    search = request.args.get("search", "").strip()
    selected_status = request.args.get("status", "").strip()

    applications = get_applications()

    # Search by company or position
    if search:
        applications = [
            application
            for application in applications
            if search.lower() in application[1].lower()
            or search.lower() in application[2].lower()
        ]

    # Filter by status
    if selected_status:
        applications = [
            application
            for application in applications
            if application[4].lower() == selected_status.lower()
        ]

    # Dashboard statistics
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
def add():
    company = request.form["company"].strip()
    position = request.form["position"].strip()
    date_applied = request.form["date_applied"].strip()
    status = request.form["status"].strip()
    salary = request.form["salary"].strip()
    notes = request.form["notes"].strip()

    # Basic validation
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