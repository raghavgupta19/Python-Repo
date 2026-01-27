import sqlite3
import pandas as pd
import os

def load_csv_to_sqlite():
    csv_file = "yellow_line_detailed.csv"
    db_file = "metro_project.db"

    # 1. Check if the CSV exists
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found. Run crawler.py first!")
        return

    try:
        # 2. Connect to SQLite (This creates the file automatically)
        conn = sqlite3.connect(db_file)
        
        # 3. Read the CSV using Pandas
        df = pd.read_csv(csv_file)

        # 4. Requirement: Clean & Transform (Final check before DB)
        # Replacing any empty facility cells with 'None' for SQL consistency
        df['Facilities'] = df['Facilities'].fillna('None')

        # 5. Requirement: Create table and Insert data
        # 'if_exists=replace' ensures you can run this script multiple times
        df.to_sql('yellow_line_stations', conn, if_exists='replace', index=False)

        print(f"✅ Success! Data from {csv_file} is now in {db_file}")
        
        # 6. Verify: Read back from the Database
        query = "SELECT Station_Name, Facilities FROM yellow_line_stations LIMIT 3"
        result = pd.read_sql(query, conn)
        print("\n--- Sample from Database ---")
        print(result)

        conn.close()

    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    load_csv_to_sqlite()