from config import setup_logging
from data_pipeline import DataPipeline
import sqlite3
import pandas as pd

def run_insights():
    conn = sqlite3.connect("business_insights.db")
    print("\n" + "="*50)
    print("        🚀 DEEP BUSINESS INSIGHTS REPORT")
    print("="*50)
    
    # --- INSIGHT 1: Data Integrity Check (The "No Email is Invalid" message) ---
    query_valid = "SELECT COUNT(*) FROM users WHERE email NOT LIKE '%@%'"
    invalid_count = pd.read_sql(query_valid, conn).iloc[0, 0]
    if invalid_count == 0:
        print("✅ Insight 1: Data Quality Audit - All emails are valid (contain '@').")
    else:
        print(f"❌ Insight 1: Data Quality Audit - {invalid_count} invalid emails found.")

    # --- INSIGHT 2: Geographic Market Concentration ---
    query_geo = "SELECT city, COUNT(*) as user_count FROM users GROUP BY city ORDER BY user_count DESC"
    print("\n📍 Insight 2: User Distribution by City")
    print(pd.read_sql(query_geo, conn))

    # --- INSIGHT 3: Email Provider Segmentation (Marketing Persona) ---
    # This extracts the domain (e.g., .biz, .com) to see who the users are
    query_domain = """
    SELECT 
        SUBSTR(email, INSTR(email, '.') + 1) as domain_extension, 
        COUNT(*) as total 
    FROM users 
    GROUP BY domain_extension
    ORDER BY total DESC
    """
    print("\n📧 Insight 3: Email Domain Breakdown (Persona Analysis)")
    print(pd.read_sql(query_domain, conn))

    # --- INSIGHT 4: Logistics & Shipping Format ---
    # Identifies users with complex/extended zipcodes
    query_zip = "SELECT COUNT(*) as extended_zips FROM users WHERE zipcode LIKE '%-%'"
    extended_zips = pd.read_sql(query_zip, conn).iloc[0, 0]
    print(f"\n📬 Insight 4: Logistics - {extended_zips} users use extended (9-digit) zipcodes.")

    # --- INSIGHT 5: Top Tier Users (Alphabetical Audit) ---
    # Simple check for user naming conventions or identifying specific ranges
    query_top = "SELECT name, email FROM users ORDER BY name LIMIT 3"
    print("\n👤 Insight 5: Top 3 Users (Alphabetical Directory)")
    print(pd.read_sql(query_top, conn))

    print("\n" + "="*50)
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
        if clean_df is not None and not clean_df.empty:
            pipeline.load(clean_df)
            run_insights()
        else:
            print("Transformation resulted in no valid data.")