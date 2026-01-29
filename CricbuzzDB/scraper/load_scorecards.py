import sqlite3
import pandas as pd
import os

DB = "cricket.db"

def get_match_id(cur, match_dir):
    info_path = os.path.join(match_dir, "info_segment.csv")
    info = pd.read_csv(info_path)

    match_name = info.loc[info["Info"] == "Match", "Value"].values[0]

    cur.execute(
        "SELECT match_id FROM matches WHERE match_name = ?",
        (match_name,)
    )
    row = cur.fetchone()
    if not row:
        raise ValueError(f"❌ Match not found: {match_name}")

    return row[0]


def get_player_id(cur, player_name):
    clean = player_name.split("(")[0].strip()
    cur.execute(
        "SELECT player_id FROM players WHERE player_name LIKE ?",
        (clean + "%",)
    )
    return cur.fetchone()[0]


def load_batting(match_dir):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    match_id = get_match_id(cur, match_dir)
    df = pd.read_csv(os.path.join(match_dir, "batting_scorecard.csv"))

    for _, r in df.iterrows():
        player_id = get_player_id(cur, r["Player"])

        cur.execute("""
            INSERT OR IGNORE INTO batting_scorecard
            (match_id, player_id, runs, balls, fours, sixes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            match_id,
            player_id,
            int(r["Runs"]),
            int(r["Balls"]),
            int(r["4s"]),
            int(r["6s"])
        ))

    conn.commit()
    conn.close()


def load_bowling(match_dir):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    match_id = get_match_id(cur, match_dir)
    df = pd.read_csv(os.path.join(match_dir, "bowling_scorecard.csv"))

    for _, r in df.iterrows():
        player_id = get_player_id(cur, r["Bowler"])

        cur.execute("""
    INSERT OR IGNORE INTO bowling_scorecard
    (match_id, player_id, overs, runs, wickets)
    VALUES (?, ?, ?, ?, ?)
""", (
    match_id,
    player_id,
    float(r["Overs"]),
    int(r["Runs"]),
    int(r["Wickets"])
))


    conn.commit()
    conn.close()


def load_all_scorecards():
    for folder in os.listdir("matches"):
        path = os.path.join("matches", folder)
        if os.path.isdir(path):
            load_batting(path)
            load_bowling(path)

    print("✅ Batting & Bowling scorecards loaded")
