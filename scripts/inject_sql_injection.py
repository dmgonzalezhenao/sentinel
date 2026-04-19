"""
Anomaly Injector - Phase 2: SQL Injection.

Injects malicious SQL patterns into the log messages to simulate 
SQL injection attempts against the application.
"""

import pandas as pd
import random
from datetime import datetime, timedelta

# File paths
FILE_PATH = "..\\data\\raw\\sentinel_report_20260414_1205_brute_force.csv"
OUTPUT_PATH = "..\\data\\raw\\sentinel_report_20260414_1205_sql_injection.csv"

# Date range configuration
MIN_DATE = datetime.strptime("2026-02-24 18:15:19", "%Y-%m-%d %H:%M:%S")
MAX_DATE = datetime.strptime("2026-03-26 18:51:49", "%Y-%m-%d %H:%M:%S")
TOTAL_SECONDS_RANGE = int((MAX_DATE - MIN_DATE).total_seconds())

# Define common SQL injections
SQL_PAYLOADS = [
    "admin' --",
    "' OR 1=1 --",
    "'; DROP TABLE users; --",
    "UNION SELECT username, password FROM users--",
    "1' ORDER BY 1--",
    "' AND 1=0 UNION SELECT NULL, @@version--"
]

def inject_sql_injection() -> None:
    """
    Injects malicious SQL query patterns into the database service logs.

    This function simulates SQL injection attempts by picking random malicious 
    payloads (e.g., OR 1=1, UNION SELECT) and inserting them into the 'Message' 
    field of the logs. It simulates a slightly higher 'Process Time' than 
    standard queries to reflect the overhead of complex malicious statements. 
    The resulting data is merged, sorted by timestamp, and IDs are regenerated 
    to maintain dataset integrity.

    Returns:
        None

    Raises:
        FileNotFoundError: If the input file from the previous phase is missing.
    """
    try:
        # Create the DataFrame
        df = pd.read_csv(FILE_PATH)
        
        # Create new records list
        new_records = []

        # Generate 40 SQL injection attacks
        for _ in range(40):
            # Choose a random time
            random_start_second = random.randint(0, TOTAL_SECONDS_RANGE)
            attack_time = MIN_DATE + timedelta(seconds=random_start_second)

            # Choose one of the injections
            payload = random.choice(SQL_PAYLOADS)
            
            # Create log WITHOUT ID
            log = {
                "Service name": "Database",
                "Log Level": "WARNING",
                "Message": f"Suspicious query detected: {payload}",
                "Risk Score": random.randint(70, 99),
                "Is Anomaly": True,
                "Timestamp": attack_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Process Time": random.randint(20, 45) 
            }

            # Append log to list
            new_records.append(log)

        # Create a DataFrame with SQL injections
        df_sql = pd.DataFrame(new_records)

        # Concatenate both DafaTrames
        df_final = pd.concat([df, df_sql], ignore_index=True)

        # Sort by Timestamp and drop index
        df_final = df_final.sort_values(by='Timestamp').reset_index(drop=True)

        # Transform IDs
        df_final['ID'] = range(1, len(df_final) + 1)

        # Save DataFrame without index
        df_final.to_csv(OUTPUT_PATH, index=False)
        print(f"Phase 2 completed: Injected {len(df_sql)} SQL Injection logs.")
        print(f"Total records in dataset: {len(df_final)}")

    # Exception if there's no file
    except FileNotFoundError:
        print(f"Error: {FILE_PATH} not found.")

# Execute script
if __name__ == "__main__":
    inject_sql_injection()