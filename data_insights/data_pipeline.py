import requests
import pandas as pd
import sqlite3
import logging

class DataPipeline:
    def __init__(self, api_url):
        self.api_url = api_url
        self.db_name = "business_insights.db"

    # MUST BE NAMED 'extract' to match main.py
    def extract(self):
        try:
            logging.info("Extracting data from API...")
            response = requests.get(self.api_url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"API Extraction Error: {e}")
            return None

    def transform(self, data):
        # ... (your transformation logic here)
        # Ensure this method is named 'transform'
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
        
        # Validations
        df = df.drop_duplicates(subset=['user_id'])
        df = df[df['email'].str.contains("@", na=False)]
        df = df[df['city'].notna() & (df['city'] != "")]
        df = df[df['zipcode'].astype(str).str.len() >= 5]
        
        return df

    def load(self, df):
        # Ensure this method is named 'load'
        df.to_csv("transformed_data.csv", index=False)
        conn = sqlite3.connect(self.db_name)
        df.to_sql('users', conn, if_exists='replace', index=False)
        conn.close()