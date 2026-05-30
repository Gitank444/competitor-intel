import sqlite3

DB_PATH = "competitor_intel.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS github_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competitor TEXT,
            repo TEXT,
            dependencies TEXT,
            file_structure TEXT,
            captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docs_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competitor TEXT,
            url TEXT,
            content TEXT,
            captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competitor TEXT,
            jobs_raw TEXT,
            captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("DB initialized")

def get_last_snapshot(table, competitor):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM {table} WHERE competitor=? ORDER BY captured_at DESC LIMIT 1",
        (competitor,)
    )
    row = cursor.fetchone()
    conn.close()
    return row

def save_snapshot(table, competitor, **kwargs):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    columns = ", ".join(["competitor"] + list(kwargs.keys()))
    placeholders = ", ".join(["?"] * (len(kwargs) + 1))
    values = [competitor] + list(kwargs.values())
    cursor.execute(
        f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
        values
    )
    conn.commit()
    conn.close()