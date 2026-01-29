import sqlite3
import pandas as pd
import re
from datetime import datetime

DB = "cricket.db"


def extract_match_type(match_name):
    if "T20" in match_name:
        return "T20"
    if "ODI" in match_name:
        return "ODI"
    if "Test" in match_name:
        return "TEST"
    return "UNKNOWN"


def parse_match_date(date_str):
    # "Wed, Jan 21"
    try:
        clean = date_str.split(",")[1].strip()
        return datetime.strptime(clean, "%b %d").date().replace(year=2026)
    except:
        return None


def get_team_id(cur, team_code):
    cur.execute(
        "SELECT team_id FROM teams WHERE team_code=?",
        (team_code,)
    )
    return cur.fetchone()[0]


def insert_match(folder):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    info = pd.read_csv(f"{folder}/info_segment.csv")
    result = pd.read_csv(f"{folder}/match_result.csv").iloc[0]

    match_name = info.loc[info["Info"] == "Match", "Value"].values[0]
    date_raw = info.loc[info["Info"] == "Date", "Value"].values[0]
    city = info.loc[info["Info"] == "City", "Value"].values[0]

    match_date = parse_match_date(date_raw)
    match_type = extract_match_type(match_name)

    team1_id = get_team_id(cur, result["Team 1 name code"])
    team2_id = get_team_id(cur, result["Team 2 name code"])

    cur.execute("""
        INSERT OR IGNORE INTO matches
        (match_name, match_date, match_type, venue, team1_id, team2_id, result)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        match_name,
        match_date,
        match_type,
        city,
        team1_id,
        team2_id,
        result["Result"]
    ))

    conn.commit()
    conn.close()

    print(f"✅ Match loaded: {match_name}")

import os

def load_all_matches():
    for folder in os.listdir("matches"):
        path = os.path.join("matches", folder)
        if os.path.isdir(path):
            insert_match(path)

    print("✅ All matches loaded successfully")
