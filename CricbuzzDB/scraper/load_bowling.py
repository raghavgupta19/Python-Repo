import os
import sqlite3
import pandas as pd
import re

DB = "cricket.db"

def insert_bowling(match_id, folder):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    df = pd.read_csv(os.path.join(folder, "bowling_scorecard.csv"))

    for _, row in df.iterrows():
        name = re.sub(r"\(.*?\)", "", row["Bowler"]).strip()

        cur.execute("SELECT player_id FROM players WHERE player_name=?", (name,))
        res = cur.fetchone()
        if not res:
            continue

        player_id = res[0]

        cur.execute("""
            INSERT OR IGNORE INTO bowling_scorecard
            (match_id, player_id, overs, runs_conceded, wickets, economy)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            match_id,
            player_id,
            float(row["Overs"]),
            int(row["Runs"]),
            int(row["Wickets"]),
            round(int(row["Runs"]) / float(row["Overs"]), 2) if float(row["Overs"]) else None
        ))

    conn.commit()
    conn.close()
