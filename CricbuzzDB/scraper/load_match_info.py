import sqlite3
import pandas as pd
import os

DB = "cricket.db"

def get_match_id(cur, match_dir):
    info = pd.read_csv(os.path.join(match_dir, "info_segment.csv"))
    match_name = info.loc[info["Info"] == "Match", "Value"].values[0]

    cur.execute(
        "SELECT match_id FROM matches WHERE match_name = ?",
        (match_name,)
    )
    return cur.fetchone()[0]


def load_match_info(match_dir):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    match_id = get_match_id(cur, match_dir)
    df = pd.read_csv(os.path.join(match_dir, "info_segment.csv"))

    for _, row in df.iterrows():
        key = row["Info"].strip()
        value = str(row["Value"]).strip()

        cur.execute("""
            INSERT OR IGNORE INTO match_info_raw
            (match_id, info_key, info_value)
            VALUES (?, ?, ?)
        """, (match_id, key, value))

    conn.commit()
    conn.close()


def load_all_match_info():
    for folder in os.listdir("matches"):
        path = os.path.join("matches", folder)
        if os.path.isdir(path):
            load_match_info(path)

    print("✅ Match info (umpires, city, toss, etc.) loaded")
