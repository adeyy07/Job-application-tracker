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

    cursor.execute("""
        SELECT * FROM applications
        ORDER BY date_applied DESC
    """)

    applications = cursor.fetchall()
    conn.close()

    return applications


def search_applications(keyword):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM applications
        WHERE company LIKE ? OR position LIKE ?
        ORDER BY date_applied DESC
    """, (f"%{keyword}%", f"%{keyword}%"))

    results = cursor.fetchall()
    conn.close()

    return results


def filter_by_status(status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM applications
        WHERE LOWER(status) = LOWER(?)
        ORDER BY date_applied DESC
    """, (status,))

    results = cursor.fetchall()
    conn.close()

    return results


def update_status(application_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET status = ?
        WHERE id = ?
    """, (new_status, application_id))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated


def delete_application(application_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM applications
        WHERE id = ?
    """, (application_id,))

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    return deleted


def get_statistics():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM applications
        GROUP BY status
    """)

    status_counts = cursor.fetchall()

    conn.close()

    return total, status_counts