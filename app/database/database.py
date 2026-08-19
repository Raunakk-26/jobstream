import sqlite3
from pathlib import Path


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = BASE_DIR / "jobs.db"


# ============================================================
# CONNECTION
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        str(DATABASE_PATH)
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# CREATE TABLES
# ============================================================

def create_jobs_table():

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            employment_type TEXT,
            salary TEXT,
            seniority TEXT,
            description TEXT,
            url TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            published_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS ingestion_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            fetched INTEGER NOT NULL,
            new_jobs INTEGER NOT NULL,
            duplicates INTEGER NOT NULL,
            fallback_used INTEGER NOT NULL,
            error TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    connection.close()


# ============================================================
# SAVE JOB
# ============================================================

def save_job(job):

    connection = get_connection()

    cursor = connection.execute("""
        INSERT OR IGNORE INTO jobs (
            title,
            company,
            location,
            employment_type,
            salary,
            seniority,
            description,
            url,
            source,
            published_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job["title"],
        job["company"],
        job["location"],
        job["employment_type"],
        job["salary"],
        job["seniority"],
        job["description"],
        job["url"],
        job["source"],
        job["published_at"]
    ))

    connection.commit()

    inserted = cursor.rowcount == 1

    connection.close()

    return inserted


# ============================================================
# SAVE INGESTION REPORT
# ============================================================

def save_ingestion_report(report):

    connection = get_connection()

    connection.execute("""
        INSERT INTO ingestion_runs (
            source,
            fetched,
            new_jobs,
            duplicates,
            fallback_used,
            error
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        report["source"],
        report["fetched"],
        report["new_jobs"],
        report["duplicates"],
        int(report["fallback_used"]),
        report["error"]
    ))

    connection.commit()

    connection.close()


# ============================================================
# GET LATEST INGESTION
# ============================================================

def get_latest_ingestion():

    connection = get_connection()

    report = connection.execute("""
        SELECT
            source,
            fetched,
            new_jobs,
            duplicates,
            fallback_used,
            error,
            created_at
        FROM ingestion_runs
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()

    connection.close()

    return report