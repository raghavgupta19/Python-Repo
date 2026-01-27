from config import setup_logging
from data_pipeline import DataPipeline
import sqlite3
import pandas as pd

def run_insights():
    conn = sqlite3.connect("business_insights.db")
    print("\n--- SQL BUSINESS INSIGHTS ---")
    
    # Query 1: Count users per city
    query1 = "SELECT city, COUNT(*) as total_users FROM users GROUP BY city"
    print("\nUser Count by City:")
    print(pd.read_sql(query1, conn))

    # Query 2: List all users in a specific zipcode format (Example insight)
    query2 = "SELECT name, email FROM users WHERE zipcode LIKE '%-%'"
    print("\nUsers with Long-Format Zipcodes:")
    print(pd.read_sql(query2, conn))
    
    conn.close()

if __name__ == "__main__":
    # Setup
    setup_logging()
    API_URL = "https://jsonplaceholder.typicode.com/users"
    pipeline = DataPipeline(API_URL)

    # Execution
    raw_data = pipeline.extract()
    if raw_data:
        clean_df = pipeline.transform(raw_data)
        pipeline.load(clean_df)
        run_insights()