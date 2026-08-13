from database import create_table, add_application, get_applications


def add_new_application():
    print("\nAdd New Job Application")

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


def view_applications():
    applications = get_applications()

    if not applications:
        print("\nNo applications found.")
        return

    print("\nJob Applications")
    print("-" * 80)

    for application in applications:
        print(f"ID: {application[0]}")
        print(f"Company: {application[1]}")
        print(f"Position: {application[2]}")
        print(f"Date Applied: {application[3]}")
        print(f"Status: {application[4]}")
        print(f"Salary: {application[5]}")
        print(f"Notes: {application[6]}")
        print("-" * 80)


def main():
    create_table()

    while True:
        print("\nJOB APPLICATION TRACKER")
        print("1. Add application")
        print("2. View applications")
        print("3. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_new_application()
        elif choice == "2":
            view_applications()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
