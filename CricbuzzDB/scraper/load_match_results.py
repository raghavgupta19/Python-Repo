import sqlite3
import pandas as pd
import os

DB = "cricket.db"

def insert_match_result(match_dir):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # ---------- paths ----------
    result_csv = os.path.join(match_dir, "match_result.csv")
    info_csv = os.path.join(match_dir, "info_segment.csv")

    if not os.path.exists(result_csv) or not os.path.exists(info_csv):
        conn.close()
        return

    df = pd.read_csv(result_csv)
    info_df = pd.read_csv(info_csv)

    # ---------- get match name ----------
    match_name = info_df.loc[
        info_df["Info"] == "Match", "Value"
    ].values[0]

    cur.execute(
        "SELECT match_id FROM matches WHERE match_name = ?",
        (match_name,)
    )
    res = cur.fetchone()
    if not res:
        conn.close()
        raise ValueError(f"❌ Match not found: {match_name}")

    match_id = res[0]

    row = df.iloc[0]

    # ---------- player of match (nullable) ----------
    pom_id = None
    if pd.notna(row["Player of Match"]):
        pom_name = row["Player of Match"].strip()
        cur.execute(
            "SELECT player_id FROM players WHERE player_name = ?",
            (pom_name,)
        )
        pom = cur.fetchone()
        if pom:
            pom_id = pom[0]

    # ---------- teams ----------
    cur.execute(
        "SELECT team_id FROM teams WHERE team_code = ?",
        (row["Team 1 name code"],)
    )
    team1_id = cur.fetchone()[0]

    cur.execute(
        "SELECT team_id FROM teams WHERE team_code = ?",
        (row["Team 2 name code"],)
    )
    team2_id = cur.fetchone()[0]

    # ---------- insert ----------
    cur.execute("""
        INSERT OR IGNORE INTO match_results
        (match_id, result, player_of_match, team1_id, team2_id, team1_score, team2_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        match_id,
        row["Result"],
        pom_id,
        team1_id,
        team2_id,
        row["Team 1 Score"],
        row["Team 2 Score"]
    ))

    conn.commit()
    conn.close()

    print(f"✅ Match result loaded: {match_name}")
