# database.py

import sqlite3
import uuid
from typing import Optional, Tuple

DB_FILE = "analysis_results.db"

def init_db():
    """Initializes the database and creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_jobs (
            job_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            filename TEXT,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()

def create_job(filename: str) -> str:
    """Creates a new job entry in the database and returns the job ID."""
    job_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analysis_jobs (job_id, status, filename, result) VALUES (?, ?, ?, ?)",
        (job_id, "pending", filename, None)
    )
    conn.commit()
    conn.close()
    return job_id

def update_job_result(job_id: str, result: str):
    """Updates a job with the analysis result and sets status to 'completed'."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE analysis_jobs SET status = ?, result = ? WHERE job_id = ?",
        ("completed", result, job_id)
    )
    conn.commit()
    conn.close()

def get_job_status(job_id: str) -> Optional[Tuple[str, Optional[str]]]:
    """Retrieves the status and result of a job."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT status, result FROM analysis_jobs WHERE job_id = ?",
        (job_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row if row else None