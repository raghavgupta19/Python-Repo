import sqlite3

DB = "cricket.db"

def insert_team(code, name):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO teams (team_code, team_name)
        VALUES (?, ?)
    """, (code, name))

    conn.commit()
    conn.close()
