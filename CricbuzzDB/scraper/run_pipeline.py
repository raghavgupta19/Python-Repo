import os
import sqlite3
from load_players import insert_players
from load_matches import insert_match
from load_match_info import insert_match_info
from load_batting import insert_batting
from load_bowling import insert_bowling
from load_teams import insert_team

DB = "cricket.db"
BASE = "matches"

# --- STEP 0: Ensure teams exist ---
TEAMS = {
    "IND": "India",
    "NZ": "New Zealand",
    "ENG": "England",
    "SL": "Sri Lanka",
    "IRE": "Ireland",
    "ITA": "Italy",
    "AFG": "Afghanistan",
    "WI": "West Indies"
}

for code, name in TEAMS.items():
    insert_team(code, name)

# --- STEP 1: Load players ---
for f in os.listdir(BASE):
    p = os.path.join(BASE, f, "playing_11_profiles_detailed.csv")
    if os.path.exists(p):
        insert_players(p)

# --- STEP 2: Load matches + dependent tables ---
for f in os.listdir(BASE):
    folder = os.path.join(BASE, f)
    if not os.path.isdir(folder):
        continue

    match_id = insert_match(folder)
    insert_match_info(match_id, folder)
    insert_batting(match_id, folder)
    insert_bowling(match_id, folder)

print("✅ Full pipeline executed safely")
