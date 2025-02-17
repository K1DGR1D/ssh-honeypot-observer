import sqlite3
import os

DB_FILE = "../honeypot_logs.db"

def test_database_exists():
    assert os.path.exists(DB_FILE)

def test_can_insert_data():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO attack_logs (ip_address, username, password) VALUES ('192.168.1.2', 'testuser', 'testpass')")
    conn.commit()
    
    cur.execute("SELECT * FROM attack_logs WHERE ip_address='192.168.1.2'")
    result = cur.fetchone()
    conn.close()

    assert result is not None
