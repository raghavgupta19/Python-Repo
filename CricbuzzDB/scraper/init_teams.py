from load_teams import insert_team

teams = {
    "IND": "India",
    "NZ": "New Zealand",
    "ENG": "England",
    "SL": "Sri Lanka",
    "IRE": "Ireland",
    "ITA": "Italy",
    "AFG": "Afghanistan",
    "WI": "West Indies"
}

for code, name in teams.items():
    insert_team(code, name)

print("✅ Teams inserted safely")
