import sqlite3
import pandas as pd
from datetime import datetime

DB = "cricket.db"

TEAM_CODE_MAP = {
    "India": "IND",
    "New Zealand": "NZ",
    "Australia": "AUS",
    "England": "ENG",
    "South Africa": "SA",
    "Pakistan": "PAK",
    "Sri Lanka": "SL",
    "Bangladesh": "BAN",
    "West Indies": "WI",
    "Afghanistan": "AFG",
    "Ireland": "IRE",
    "Scotland": "SCO",
    "Netherlands": "NED",
    "Zimbabwe": "ZIM",
    "Italy": "ITA",          # ✅ add this
    "United States": "USA",  # future-safe
    "Nepal": "NEP",
    "Oman": "OMA",
    "UAE": "UAE"
}


def parse_birth_date(born):
    if pd.isna(born):
        return None
    try:
        clean = born.split("(")[0].strip()
        return datetime.strptime(clean, "%B %d, %Y").date()
    except:
        return None


def get_or_create_team(cur, team_name):
    team_code = TEAM_CODE_MAP.get(team_name)

    if not team_code:
        raise ValueError(f"❌ Unknown team name: {team_name}")

    cur.execute(
        "INSERT OR IGNORE INTO teams (team_code, team_name) VALUES (?, ?)",
        (team_code, team_name)
    )

    cur.execute(
        "SELECT team_id FROM teams WHERE team_code=?",
        (team_code,)
    )
    return cur.fetchone()[0]


def get_or_create_role(cur, role_name):
    cur.execute(
        "INSERT OR IGNORE INTO player_roles (role_name) VALUES (?)",
        (role_name,)
    )

    cur.execute(
        "SELECT role_id FROM player_roles WHERE role_name=?",
        (role_name,)
    )
    return cur.fetchone()[0]


def insert_players(csv_path):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        player_name = row["Name"].strip()
        team_name = row["Team"].strip()
        role_name = row["Role"].strip()

        birth_date = parse_birth_date(row["Born"])
        batting_style = row["Batting Style"]
        bowling_style = row["Bowling Style"]

        team_id = get_or_create_team(cur, team_name)

        cur.execute("""
            INSERT OR IGNORE INTO players
            (player_name, team_id, birth_date, batting_style, bowling_style)
            VALUES (?, ?, ?, ?, ?)
        """, (player_name, team_id, birth_date, batting_style, bowling_style))

        cur.execute("""
            SELECT player_id FROM players
            WHERE player_name=? AND team_id=?
        """, (player_name, team_id))

        player_id = cur.fetchone()[0]

        role_id = get_or_create_role(cur, role_name)

        cur.execute("""
            INSERT OR IGNORE INTO player_role_map
            (player_id, role_id)
            VALUES (?, ?)
        """, (player_id, role_id))

    conn.commit()
    conn.close()

    print("✅ Players with roles loaded successfully")
