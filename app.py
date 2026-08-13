from database import (
    create_table,
    add_application,
    get_applications,
    search_applications,
    filter_by_status,
    update_status,
    delete_application,
    get_statistics
)


def display_applications(applications):
    if not applications:
        print("\nNo applications found.")
        return

    print("\nJOB APPLICATIONS")
    print("-" * 70)

    for application in applications:
        print(f"ID: {application[0]}")
        print(f"Company: {application[1]}")
        print(f"Position: {application[2]}")
        print(f"Date Applied: {application[3]}")
        print(f"Status: {application[4]}")
        print(f"Salary: {application[5]}")
        print(f"Notes: {application[6]}")
        print("-" * 70)


def add_new_application():
    print("\nADD NEW JOB APPLICATION")

    company = input("Company: ")
    position = input("Position: ")
    date_applied = input("Date applied (YYYY-MM-DD): ")
    status = input("Status (Applied / Interview / Offer / Rejected): ")
    salary = input("Salary or salary range: ")
    notes = input("Notes: ")

    add_application(
        company,
        position,
        date_applied,
        status,
        salary,
        notes
    )

    print("\nApplication saved successfully.")


def view_all_applications():
    display_applications(get_applications())


def search_jobs():
    keyword = input("\nEnter company or position to search: ")
    results = search_applications(keyword)
    display_applications(results)


def filter_jobs():
    status = input(
        "\nEnter status (Applied / Interview / Offer / Rejected): "
    )

    results = filter_by_status(status)
    display_applications(results)


def update_job_status():
    application_id = input("\nEnter application ID: ")
    new_status = input(
        "Enter new status (Applied / Interview / Offer / Rejected): "
    )

    if not application_id.isdigit():
        print("Invalid ID.")
        return

    updated = update_status(int(application_id), new_status)

    if updated:
        print("Application status updated successfully.")
    else:
        print("Application not found.")


def remove_application():
    application_id = input("\nEnter application ID to delete: ")

    if not application_id.isdigit():
        print("Invalid ID.")
        return

    deleted = delete_application(int(application_id))

    if deleted:
        print("Application deleted successfully.")
    else:
        print("Application not found.")


def show_statistics():
    total, status_counts = get_statistics()

    print("\nAPPLICATION STATISTICS")
    print("-" * 30)
    print(f"Total applications: {total}")

    for status, count in status_counts:
        print(f"{status}: {count}")


def main():
    create_table()

    while True:
        print("\nJOB APPLICATION TRACKER")
        print("1. Add application")
        print("2. View applications")
        print("3. Search applications")
        print("4. Filter by status")
        print("5. Update application status")
        print("6. Delete application")
        print("7. View statistics")
        print("8. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_new_application()

        elif choice == "2":
            view_all_applications()

        elif choice == "3":
            search_jobs()

        elif choice == "4":
            filter_jobs()

        elif choice == "5":
            update_job_status()

        elif choice == "6":
            remove_application()

        elif choice == "7":
            show_statistics()

        elif choice == "8":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()