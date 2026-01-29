import sqlite3, pandas as pd, re

DB = "cricket.db"

def insert_batting(match_id, folder):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    df = pd.read_csv(f"{folder}/batting_scorecard.csv")

    for _, row in df.iterrows():
        raw = row["Player"]
        is_captain = "(c)" in raw.lower()
        is_wk = "(wk)" in raw.lower()
        name = re.sub(r"\(.*?\)", "", raw).strip()

        cur.execute("SELECT player_id FROM players WHERE player_name=?", (name,))
        player_id = cur.fetchone()[0]

        balls = int(row["Balls"])
        runs = int(row["Runs"])
        sr = round((runs/balls)*100,2) if balls else None

        cur.execute("""
            INSERT OR IGNORE INTO batting_scorecard
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            match_id, player_id, runs, balls,
            row["4s"], row["6s"], sr,
            is_captain, is_wk
        ))

    conn.commit()
    conn.close()
