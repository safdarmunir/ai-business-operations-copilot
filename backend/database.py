import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "copilot.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        route TEXT,
        filename TEXT,
        created_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        question TEXT NOT NULL,
        report_path TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def save_chat(role, content, route=None, filename=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chat_history (role, content, route, filename, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        role,
        content,
        route,
        filename,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_chat_history(limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT role, content, route, filename, created_at
    FROM chat_history
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "role": row[0],
            "content": row[1],
            "route": row[2],
            "filename": row[3],
            "created_at": row[4]
        }
        for row in rows
    ][::-1]


def clear_chat_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM chat_history")

    conn.commit()
    conn.close()


def save_report(filename, question, report_path):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reports (filename, question, report_path, created_at)
    VALUES (?, ?, ?, ?)
    """, (
        filename,
        question,
        report_path,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_reports(limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT filename, question, report_path, created_at
    FROM reports
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "filename": row[0],
            "question": row[1],
            "report_path": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]