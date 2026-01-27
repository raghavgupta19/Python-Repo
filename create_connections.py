import sqlite3

connections = [
    ("Samaypur Badli", "Rohini Sector 18, 19", 1.5, 3, "Yellow Line"),
    ("Rohini Sector 18, 19", "Haiderpur Badli Mor", 1.2, 2, "Yellow Line"),
    ("Haiderpur Badli Mor", "Jahangirpuri", 1.3, 3, "Yellow Line"),
    ("Jahangirpuri", "Adarsh Nagar", 1.4, 3, "Yellow Line"),
    ("Adarsh Nagar", "Azadpur", 1.2, 2, "Yellow Line"),
    ("Azadpur", "Model Town", 1.1, 2, "Yellow Line"),
    ("Model Town", "GTB Nagar", 1.0, 2, "Yellow Line"),
    ("GTB Nagar", "Vishwavidyalaya", 0.9, 2, "Yellow Line"),
    ("Vishwavidyalaya", "Vidhan Sabha", 1.2, 3, "Yellow Line"),
    ("Vidhan Sabha", "Civil Lines", 1.3, 3, "Yellow Line"),
    ("Civil Lines", "Kashmere Gate", 1.1, 2, "Yellow Line"),
    ("Kashmere Gate", "Chandni Chowk", 1.2, 3, "Yellow Line"),
    ("Chandni Chowk", "Chawri Bazar", 0.8, 2, "Yellow Line"),
    ("Chawri Bazar", "New Delhi", 1.0, 2, "Yellow Line"),
    ("New Delhi", "Rajiv Chowk", 0.9, 2, "Yellow Line"),
    ("Rajiv Chowk", "Patel Chowk", 1.1, 2, "Yellow Line"),
    ("Patel Chowk", "Central Secretariat", 1.0, 2, "Yellow Line"),
    ("Central Secretariat", "Udyog Bhawan", 0.8, 2, "Yellow Line"),
    ("Udyog Bhawan", "Lok Kalyan Marg", 1.1, 2, "Yellow Line"),
    ("Lok Kalyan Marg", "Jor Bagh", 1.2, 3, "Yellow Line"),
    ("Jor Bagh", "INA", 1.1, 2, "Yellow Line"),
    ("INA", "AIIMS", 0.8, 2, "Yellow Line"),
    ("AIIMS", "Green Park", 1.0, 2, "Yellow Line"),
    ("Green Park", "Hauz Khas", 1.1, 2, "Yellow Line"),
    ("Hauz Khas", "Malviya Nagar", 1.2, 3, "Yellow Line"),
    ("Malviya Nagar", "Saket", 1.1, 2, "Yellow Line"),
    ("Saket", "Qutub Minar", 1.3, 3, "Yellow Line"),
    ("Qutub Minar", "Chhatarpur", 1.7, 3, "Yellow Line"),
    ("Chhatarpur", "Sultanpur", 1.6, 3, "Yellow Line"),
    ("Sultanpur", "Ghitorni", 1.5, 3, "Yellow Line"),
    ("Ghitorni", "Arjan Garh", 1.7, 3, "Yellow Line"),
    ("Arjan Garh", "Guru Dronacharya", 1.6, 3, "Yellow Line"),
    ("Guru Dronacharya", "Sikandarpur", 1.5, 3, "Yellow Line"),
    ("Sikandarpur", "MG Road", 1.1, 2, "Yellow Line"),
    ("MG Road", "IFFCO Chowk", 1.0, 2, "Yellow Line"),
    ("IFFCO Chowk", "HUDA City Centre", 1.3, 3, "Yellow Line"),
]


def create_connection_table():
    conn = sqlite3.connect("metro_project.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS station_connections (
            from_station TEXT,
            to_station TEXT,
            distance_km REAL,
            time_min INTEGER,
            line TEXT
        )
    """)

    cur.executemany("""
        INSERT INTO station_connections 
        VALUES (?, ?, ?, ?, ?)
    """, connections)

    conn.commit()
    conn.close()
    print("✅ station_connections table created & populated")

if __name__ == "__main__":
    create_connection_table()
