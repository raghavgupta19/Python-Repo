import sqlite3

conn = sqlite3.connect("cricket.db")
cur = conn.cursor()

cur.execute("PRAGMA foreign_keys = ON;")

# ---------------- TEAMS ----------------
cur.execute("""
CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_code TEXT UNIQUE,
    team_name TEXT
);
""")

# ---------------- PLAYERS ----------------
cur.execute("""
CREATE TABLE players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT,
    team_id INTEGER,
    birth_date DATE,
    batting_style TEXT,
    bowling_style TEXT,
    UNIQUE(player_name, team_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);
""")

# ---------------- PLAYER ROLES ----------------
cur.execute("""
CREATE TABLE player_roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE
);
""")

cur.execute("""
CREATE TABLE player_role_map (
    player_id INTEGER,
    role_id INTEGER,
    PRIMARY KEY (player_id, role_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (role_id) REFERENCES player_roles(role_id)
);
""")

# ---------------- MATCHES ----------------
cur.execute("""
CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_name TEXT,
    match_type TEXT,
    match_date DATE,
    city TEXT
);
""")

# ---------------- MATCH INFO (RAW) ----------------
cur.execute("""
CREATE TABLE match_info_raw (
    match_id INTEGER,
    info_key TEXT,
    info_value TEXT,
    PRIMARY KEY (match_id, info_key),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);
""")

# ---------------- MATCH RESULTS ----------------
cur.execute("""
CREATE TABLE match_results (
    match_id INTEGER PRIMARY KEY,
    result TEXT,
    player_of_match INTEGER,
    team1_id INTEGER,
    team2_id INTEGER,
    team1_score TEXT,
    team2_score TEXT,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_of_match) REFERENCES players(player_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id)
);
""")

# ---------------- BATTING SCORECARD ----------------
cur.execute("""
CREATE TABLE batting_scorecard (
    match_id INTEGER,
    player_id INTEGER,
    runs INTEGER,
    balls INTEGER,
    fours INTEGER,
    sixes INTEGER,
    PRIMARY KEY (match_id, player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
""")

# ---------------- BOWLING SCORECARD ----------------
cur.execute("""
CREATE TABLE bowling_scorecard (
    match_id INTEGER,
    player_id INTEGER,
    overs REAL,
    runs INTEGER,
    wickets INTEGER,
    PRIMARY KEY (match_id, player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
""")

conn.commit()
conn.close()

print("✅ Phase 1 DB setup completed successfully")
