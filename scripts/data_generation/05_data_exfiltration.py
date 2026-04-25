"""
Sentinel Data Exfiltration Module.

Simulates unauthorized data transfers by manipulating Process Time 
and Risk Score in sensitive services.
"""

# Import pandas to handle bulk of data
import pandas as pd

# Import random and datetime to set random dates
import random
from datetime import datetime, timedelta

# Paths configurations
INPUT_PATH = "..\\data\\raw\\sentinel_logs_xss_injection.csv"
OUTPUT_PATH = "..\\data\\raw\\sentinel_logs_final_dataset.csv"

# Time range configuration
MIN_DATE = datetime.strptime("2026-02-24 18:15:19", "%Y-%m-%d %H:%M:%S")
MAX_DATE = datetime.strptime("2026-03-26 18:51:49", "%Y-%m-%d %H:%M:%S")
TOTAL_SECONDS_RANGE = int((MAX_DATE - MIN_DATE).total_seconds())

# Messages for exfiltration logs
EXFIL_MESSAGES = [
    "Outbound connection established to unknown IP",
    "Large data packet transfer initiated",
    "Continuous data stream detected on port 443",
    "Backup service exporting encrypted chunks",
    "High volume database query results being piped"
]

# Messages for normal logs
NORMAL_MESSAGES = [
    "Routine database synchronization",
    "Heartbeat signal sent to monitoring node",
    "Backup integrity check: OK",
    "Standard API response sent",
    "Internal microservice communication"
]

def inject_and_balance_exfiltration() -> None:
    """
    Simulates data exfiltration attacks and balances with normal network logs.
    Targets services like 'Database-API' and 'Backup-Service' with high 
    Process Time values to create behavioral anomalies.

    Returns:
        None.

    Raises:
        FileNotFoundError: If the input file from the previous phase is missing.
    """
    try:
        # Read CSV from previous phase
        df = pd.read_csv(INPUT_PATH)

        # Define target services and new records list
        target_services = ["Database-API", "Backup-Service", "File-Storage"]
        new_records = []

        # Generate 250 Data Exfiltration Attacks (High Process Time)
        for _ in range(250):
            # Set log timestamp
            random_second = random.randint(0, TOTAL_SECONDS_RANGE)
            log_time = MIN_DATE + timedelta(seconds=random_second)
            
            # Append the log with high process time and risk score
            new_records.append({
                "Service name": random.choice(target_services),
                "Log Level": "CRITICAL",
                "Message": random.choice(EXFIL_MESSAGES),
                "Risk Score": random.randint(85, 100),
                "Is Anomaly": 1,
                "Timestamp": log_time,
                "Process Time": random.randint(2000, 8000) 
            })

        # Generate 2000 Normal Network Logs (Low Process Time)
        for _ in range(2000):
            # Set log timestamp
            random_second = random.randint(0, TOTAL_SECONDS_RANGE)
            log_time = MIN_DATE + timedelta(seconds=random_second)

            # Append the normal log
            new_records.append({
                "Service name": random.choice(target_services),
                "Log Level": "INFO",
                "Message": random.choice(NORMAL_MESSAGES),
                "Risk Score": random.randint(5, 25),
                "Is Anomaly": 0,
                "Timestamp": log_time,
                "Process Time": random.randint(1, 10) 
            })

        # Create DataFrame with data exfiltration logs
        df_new = pd.DataFrame(new_records)

        # Concatenate data exfiltration logs with input file logs
        df_final = pd.concat([df, df_new], ignore_index=True)
        
        # Transform timestamp to datetime
        df_final['Timestamp'] = pd.to_datetime(df_final['Timestamp'])

        # Sort values by timestamp and reset index
        df_final = df_final.sort_values(by='Timestamp').reset_index(drop=True)

        # Transfrom ID column
        df_final['ID'] = range(1, len(df_final) + 1)

        # Transform Is Anomaly to integers
        df_final['Is Anomaly'] = df_final['Is Anomaly'].astype(int)

        # Transfrom timestamp to string
        df_final['Timestamp'] = df_final['Timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

        # Save file and print succesful message
        df_final.to_csv(OUTPUT_PATH, index=False)
        print(f"Phase 5 Complete: Data Exfiltration injected. Final count: {len(df_final)} logs.")

    # Exception if there's no file found
    except FileNotFoundError:
        print("Error: Input file for Exfiltration module not found.")

# Execute script
if __name__ == "__main__":
    inject_and_balance_exfiltration()