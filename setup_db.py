import sqlite3

DB_FILE = "honeypot_logs.db"

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS attack_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT,
    username TEXT,
    password TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

def setup_database():
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_QUERY)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Database setup complete!")
    except Exception as e:
        print(f"❌ Error setting up database: {e}")

if __name__ == "__main__":
    setup_database()
