"""
Sentinel Data Reinforcement - Normal logs for Auth & Database.

Generates 2000 normal logs (INFO) to balance the dataset, 
ensuring the AI doesn't associate service names directly with anomalies.
"""

# Import pandas to manipulate data
import pandas as pd

# Import random and datetime to set random datetimes
import random
from datetime import datetime, timedelta

# Configurate file paths
INPUT_PATH = "..\\data\\raw\\sentinel_logs_sql_injection.csv"
OUTPUT_PATH = "..\\data\\raw\\sentinel_logs_sql_injection_balanced.csv"

# Configurate date ranges
MIN_DATE = datetime.strptime("2026-02-24 18:15:19", "%Y-%m-%d %H:%M:%S")
MAX_DATE = datetime.strptime("2026-03-26 18:51:49", "%Y-%m-%d %H:%M:%S")
TOTAL_SECONDS_RANGE = int((MAX_DATE - MIN_DATE).total_seconds())

# Create a list of messages for logs
NORMAL_MESSAGES = {
    "Authentication": [
        "User login successful",
        "Session token refreshed",
        "Logout initiated by user",
        "Password change requested",
        "MFA challenge completed"
    ],
    "Database": [
        "Query executed successfully",
        "Connection pool healthy",
        "Index maintenance completed",
        "Backup process started",
        "Transaction committed"
    ]
}

def reinforce_data() -> None:
    """
    Balances the dataset by injecting normal traffic for critical services.

    This function generates 1,000 'INFO' level logs for both 'Authentication' 
    and 'Database' services to counteract the data imbalance caused by previous 
    anomaly injections. It populates the logs with low risk scores and standard 
    process times. Finally, it performs a global chronological sort and 
    regenerates all IDs to ensure a continuous and sequential dataset structure.

    Returns:
        None

    Raises:
        FileNotFoundError: If the sql injection report from the exfiltration phase 
                           is not found.
    """
    try:
        # Read file and create new records list
        df = pd.read_csv(INPUT_PATH)
        new_records = []

        # Generate 1000 logs for each service
        for service in ["Authentication", "Database"]:
            for _ in range(1000):
                # Define time by the set range
                random_second = random.randint(0, TOTAL_SECONDS_RANGE)
                log_time = MIN_DATE + timedelta(seconds=random_second)
                
                # Create log
                log = {
                    "Service name": service,
                    "Log Level": "INFO",
                    "Message": random.choice(NORMAL_MESSAGES[service]),
                    "Risk Score": random.randint(0, 20), # Low risk
                    "Is Anomaly": 0,
                    "Timestamp": log_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Process Time": random.randint(5, 30) # Normal time
                }

                # Apend log to list
                new_records.append(log)

        # Concatenate with previous logs
        df_new = pd.DataFrame(new_records)
        df_final = pd.concat([df, df_new], ignore_index=True)

        # Sort by timestamp
        df_final['Timestamp'] = pd.to_datetime(df_final['Timestamp'])
        df_final = df_final.sort_values(by='Timestamp').reset_index(drop=True)
        
        # Set ordered IDs
        df_final['ID'] = range(1, len(df_final) + 1)
        
        # Transform timestamp to string
        df_final['Timestamp'] = df_final['Timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

        # Save file
        df_final.to_csv(OUTPUT_PATH, index=False)
        
        # Print succesful messages
        print(f"Reinforcement complete.")
        print(f"Added 2000 normal logs.")
        print(f"Dataset saved in {OUTPUT_PATH}")
        print(f"Total logs: {len(df_final)}")

    # Exception if there's no file
    except FileNotFoundError:
        print(f"Error: Can't find {INPUT_PATH}. Verify path.")

# Execute script
if __name__ == "__main__":
    reinforce_data()