"""
Sentinel Behavioral Patterns Module.

Simulates progressive attacks: 
1. Brute Force: First attempts are Normal (0), subsequent bursts are Anomalies (1).
2. Data Exfiltration: Small transfers are Normal (0), rapid spikes are Anomalies (1).
"""
# Import pandas to read and save DataFrames in csv files
import pandas as pd

# Import random to set random data
import random

# Import datetime and timedelta for hinting
from datetime import datetime, timedelta

# Import os to access to csv files
import os

# --- PATH CONFIGURATION ---
current_script_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_script_path)
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
raw_data_path = os.path.join(project_root, "data", "raw")

# Define input and ouput files names
INPUT_FILE = os.path.join(raw_data_path, "sentinel_logs_data_exfiltration.csv")
OUTPUT_FILE = os.path.join(raw_data_path, "sentinel_logs_final_behavioral.csv")

def inject_behavioral_patterns() -> None:
    try:
        # Read csv from input file and create a new records list
        df = pd.read_csv(INPUT_FILE)
        new_records = []
        
        # Simulate 50 burst attacks
        for _ in range(50):
            # Random initial time for attack
            base_time = datetime.strptime("2026-03-01 10:00:00", "%Y-%m-%d %H:%M:%S") + \
                        timedelta(seconds=random.randint(0, 1000000))
            
            # The user made a mistake in the first three attempts.
            for i in range(3):
                new_records.append({
                    "Service name": "Auth-Service",
                    "Log Level": "WARNING",
                    "Message": f"Failed login attempt for user admin - retry {i+1}",
                    "Risk Score": random.randint(10, 30),
                    "Is Anomaly": 0,
                    "Timestamp": base_time + timedelta(seconds=i * 2), 
                    "Process Time": round(random.uniform(0.1, 0.5), 2)
                })
            
            # Since 4th attempt, check it as a anomaly
            for i in range(4, 8):
                new_records.append({
                    "Service name": "Auth-Service",
                    "Log Level": "ERROR",
                    "Message": f"SUSPICIOUS: Multiple login failures - retry {i}",
                    "Risk Score": random.randint(80, 100),
                    "Is Anomaly": 1,
                    "Timestamp": base_time + timedelta(seconds=i * 2 + 1),
                    "Process Time": round(random.uniform(0.1, 0.3), 2)
                })

        # Progressive exfiltration
        for _ in range(30):
            # Set initial time for exfiltration
            base_time = datetime.strptime("2026-03-10 14:00:00", "%Y-%m-%d %H:%M:%S") + \
                        timedelta(seconds=random.randint(0, 500000))
            
            # Little data transfer
            new_records.append({
                "Service name": "Database-API",
                "Log Level": "INFO",
                "Message": "Standard data export: 50KB",
                "Risk Score": 5,
                "Is Anomaly": 0,
                "Timestamp": base_time,
                "Process Time": 1.2
            })
            
            # Sudden traffic spike
            new_records.append({
                "Service name": "Database-API",
                "Log Level": "CRITICAL",
                "Message": "ALERT: Massive outbound transfer: 500MB",
                "Risk Score": 95,
                "Is Anomaly": 1,
                "Timestamp": base_time + timedelta(seconds=5), 
                "Process Time": 28.5 
            })

        # Get logs from list and concatenate them to the dataset
        df_behavioral = pd.DataFrame(new_records)
        df_final = pd.concat([df, df_behavioral], ignore_index=True)
        
        # Transform timestamp to datetime and sort logs
        df_final['Timestamp'] = pd.to_datetime(df_final['Timestamp'])
        df_final = df_final.sort_values(by=['Timestamp']).reset_index(drop=True)
        
        # Re index IDs and transform timestamp to string
        df_final['ID'] = range(1, len(df_final) + 1)
        df_final['Timestamp'] = df_final['Timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

        # Save final dataset to the output file
        df_final.to_csv(OUTPUT_FILE, index=False)
        print(f"Phase 6 Complete: Sequential patterns (Brute Force & Exfiltration) injected.")
        print(f"Final Count: {len(df_final)} logs.")

    # Exception if there's an error
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {INPUT_FILE}")

# Execute script
if __name__ == "__main__":
    inject_behavioral_patterns()