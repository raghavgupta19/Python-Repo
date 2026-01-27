import requests
import pandas as pd
import os

def extract_readable_yellow_line():
    # Targeted API for Yellow Line
    api_url = "https://backend.delhimetrorail.com/api/v2/en/station_by_line/LN2"
    
    try:
        print(f"Connecting to API and fetching Yellow Line stations...")
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        data = response.json()

        processed_data = []

        for st in data:
            # 1. Basic Extraction
            name = st.get('station_name', 'N/A').strip().title()
            code = st.get('station_code', 'N/A')
            status = st.get('status', 'Station Open')
            is_interchange = "Yes" if st.get('interchange') == True else "No"

            # 2. Advanced Extraction for Facilities
            # We check 'station_facility' and fallback to an empty list if not found
            facilities_raw = st.get('station_facility') or []
            
            if isinstance(facilities_raw, list) and len(facilities_raw) > 0:
                # Extract the 'name' from each facility dictionary
                facility_names = [f.get('name') for f in facilities_raw if f.get('name')]
                readable_facilities = ", ".join(facility_names)
            else:
                readable_facilities = "Information Not Available"

            # 3. Create the row
            processed_data.append({
                "Station_Name": name,
                "Station_Code": code,
                "Line": "Yellow Line",
                "Status": status,
                "Interchange": is_interchange,
                "Facilities": readable_facilities
            })

        # 4. Create DataFrame
        df = pd.DataFrame(processed_data)

        # Ensure the column exists even if all rows are empty (Assignment requirement)
        if "Facilities" not in df.columns:
            df["Facilities"] = "N/A"

        # 5. Save to CSV
        output_file = "yellow_line_detailed.csv"
        df.to_csv(output_file, index=False)

        print("\n--- CSV Extraction Complete ---")
        # Displaying the last column specifically to verify
        print(df[["Station_Name", "Facilities"]].head(10)) 
        print(f"\n✅ File saved to: {os.path.abspath(output_file)}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    extract_readable_yellow_line()