"""
Anomaly Injector - Phase 1: Brute Force Attack.

Injects bursts of failed authentication logs with near-identical 
timestamps to simulate brute force attacks.
"""

# Import pandas to manipulate csv files
import pandas as pd

# Imports for hinting
import random
import uuid
from datetime import datetime, timedelta

# Define file paths
FILE_PATH = "..\\data\\raw\\sentinel_report_20260414_1205.csv"
OUTPUT_PATH = "..\\data\\raw\\sentinel_report_20260414_1205_brute_force.csv"

# Cofiguration datetime limit and seconds range
MIN_DATE = datetime.strptime("2026-02-24 18:15:19", "%Y-%m-%d %H:%M:%S")
MAX_DATE = datetime.strptime("2026-03-26 18:51:49", "%Y-%m-%d %H:%M:%S")
TOTAL_SECONDS_RANGE = int((MAX_DATE - MIN_DATE).total_seconds())

def inject_brute_force():
    try:
        # Create a DataFrame with Sentinel logs data
        df = pd.read_csv(FILE_PATH)

        # Get last id from CSV
        last_id = df['ID'].max() if not df.empty else 0

        # Create a new records list and define id
        new_records = []
        current_id = last_id + 1
        
        # Simulate 5 bursts of attacks
        for _ in range(5):
            # Select start time for attack
            random_start_second = random.randint(0, TOTAL_SECONDS_RANGE - 3600)

            # Calculate a random start time
            base_time = MIN_DATE + timedelta(seconds=random_start_second)

            # Every attack has between 30 and 60 attempts
            for i in range(random.randint(30, 60)):
                # Increment timestamps by milliseconds to simulate rapid-fire attempts
                attack_time = base_time + timedelta(milliseconds=i * 200)
                
                # Create log data
                log = {
                    "ID": current_id,
                    "Service name": "Authentication",
                    "Log Level": "ERROR",
                    "Message": "Failed login attempt - User: admin",
                    "Risk Score": random.randint(80, 95),
                    "Is Anomaly": True,
                    "Timestamp": attack_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Process Time": random.randint(50, 150)
                }

                # Append log to list
                new_records.append(log)
                current_id += 1
        
        # Once loop finished, concatenate data to logs
        df_attack = pd.DataFrame(new_records)
        df_final = pd.concat([df, df_attack], ignore_index=True)
        
        # Convert Timestamp to datetime objects for accurate sorting
        df_final['Timestamp'] = pd.to_datetime(df_final['Timestamp'])
        
        # Sort chronologically from oldest to newest
        df_final = df_final.sort_values(by='Timestamp').reset_index(drop=True)
        
        # Revert Timestamp back to string format to match your original CSV style
        df_final['Timestamp'] = df_final['Timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

        df_final.to_csv(OUTPUT_PATH, index=False)
        print(f"Phase 1 completed: Injected {len(df_attack)} brute force logs.")

    except FileNotFoundError:
        print("Ensure you have file in data/raw")

if __name__ == "__main__":
    inject_brute_force()