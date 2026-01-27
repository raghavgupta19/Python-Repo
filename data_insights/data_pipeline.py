import requests
import pandas as pd
import sqlite3
import logging

class DataPipeline:
    def __init__(self, api_url):
        self.api_url = api_url
        self.db_name = "business_insights.db"

    def extract(self):
        try:
            logging.info("Extracting data from API...")
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"API Extraction Error: {e}")
            return None

    def transform(self, data):
        logging.info("Starting Transformation and Validation...")
        # Flattening nested JSON
        flattened_data = []
        for user in data:
            flattened_data.append({
                "user_id": user.get("id"),
                "name": user.get("name"),
                "email": user.get("email"),
                "city": user.get("address", {}).get("city"),
                "zipcode": user.get("address", {}).get("zipcode")
            })
        
        df = pd.DataFrame(flattened_data)

        # Applying Validation Rules
        # 1. Duplicate user_id
        df = df.drop_duplicates(subset=['user_id'])
        
        # 2. Email without @
        df = df[df['email'].str.contains("@", na=False)]
        
        # 3. City null
        df = df[df['city'].notna() & (df['city'] != "")]
        
        # 4. Zipcode < 5 characters
        df = df[df['zipcode'].astype(str).str.len() >= 5]

        logging.info(f"Transformation complete. {len(df)} records validated.")
        return df

    def load(self, df):
        try:
            # Save to CSV (Requirement)
            df.to_csv("transformed_data.csv", index=False)
            logging.info("Saved data to transformed_data.csv")

            # Save to SQLite
            conn = sqlite3.connect(self.db_name)
            df.to_sql('users', conn, if_exists='replace', index=False)
            conn.close()
            logging.info(f"Data loaded into SQLite database: {self.db_name}")
        except Exception as e:
            logging.error(f"Database Load Error: {e}")