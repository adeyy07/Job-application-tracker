import sqlite3

DB_NAME = "applications.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            date_applied TEXT NOT NULL,
            status TEXT NOT NULL,
            salary TEXT,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_application(company, position, date_applied, status, salary, notes):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications
        (company, position, date_applied, status, salary, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (company, position, date_applied, status, salary, notes))

    conn.commit()
    conn.close()


def get_applications():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications ORDER BY date_applied DESC")
    applications = cursor.fetchall()

    conn.close()
    return applications
