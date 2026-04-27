"""
Anomaly Injector - Phase 1: Brute Force Attack.

Injects bursts of failed authentication logs with near-identical 
timestamps to simulate brute force attacks.
"""

# Import pandas to manipulate csv files
import pandas as pd

# Import os to check output path exists
import os

# Imports for hinting
import random
from datetime import datetime, timedelta

# Localize script path
current_script_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_script_path)

# Define project root path
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Define data directories
raw_data_path = os.path.join(project_root, "data", "raw")
processed_data_path = os.path.join(project_root, "data", "processed")

# Create directories if don't exist
os.makedirs(raw_data_path, exist_ok=True)
os.makedirs(processed_data_path, exist_ok=True)

# Define output file's name
OUTPUT_FILE: str = str(os.path.join(raw_data_path, "sentinel_logs_brute_force.csv"))

# Cofiguration datetime limit and seconds range
MIN_DATE = datetime.strptime("2026-02-24 18:15:19", "%Y-%m-%d %H:%M:%S")
MAX_DATE = datetime.strptime("2026-03-26 18:51:49", "%Y-%m-%d %H:%M:%S")
TOTAL_SECONDS_RANGE = int((MAX_DATE - MIN_DATE).total_seconds())

def inject_brute_force() -> None:
    """
    Simulates brute force attack anomalies by injecting bursts of failed logins.

    This function reads an existing log dataset and appends multiple 'attack bursts'.
    Each burst consists of 30 to 60 failed authentication attempts occurring 
    within milliseconds of each other. The generated logs are assigned high 
    risk scores and specific process times to distinguish them from normal traffic.
    Finally, it re-indexes and sorts the entire dataset chronologically.

    Returns:
        None
    
    Raises:
        FileNotFoundError: If the source CSV file at FILE_PATH does not exist.
    """
    # Create a new records list and define id
    new_records = []
        
    # Start ID count
    current_id = 1

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
                "Process Time": round(random.uniform(5.0, 25.0), 2)
            }

            # Append log to list
            new_records.append(log)
            current_id += 1
        
    # Once loop finished, create DataFrame
    df = pd.DataFrame(new_records)
        
    # Convert Timestamp to datetime objects for accurate sorting
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
    # Sort chronologically from oldest to newest
    df = df.sort_values(by='Timestamp').reset_index(drop=True)
        
    # Revert Timestamp back to string format to match your original CSV style
    df['Timestamp'] = df['Timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Export DataFrame
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Phase 1 completed: Injected {len(df)} brute force logs.")

    # Exception if there's a permissions erorr
    except Exception as e:
        print(f"[ERROR] Could not save the file: {e}")

# Execute script
if __name__ == "__main__":
    inject_brute_force()