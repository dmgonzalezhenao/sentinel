"""
Sentinel Data Cleansing & Normalization Pipeline

This script serves as the final stage of the data preprocessing pipeline. 
It unifies disparate raw log files (synthetic attacks and real system logs) 
into a single, standardized dataset suitable for Machine Learning training.

Key Responsibilities:
1. Data Auditing: Performs a sanity check for missing columns and null values.
2. Scale Homogenization: Converts process times from milliseconds to seconds 
   where applicable to ensure a uniform temporal scale.
3. Precision Normalization: Rounds 'process_time' to 2 decimal places (ndigits=2) 
   to eliminate floating-point noise and prevent model format-bias.
4. Data Standardization: Enforces uppercase for HTTP methods and lowercase 
   for URL paths to ensure categorical consistency.
5. Deduplication: Removes redundant entries to prevent overfitting.
"""

# Import pandas to handle bulk data
import pandas as pd

# Import os to check output path
import os

def check_data_quality(df: pd.DataFrame) -> bool:
    """
    Perform a structural and integrity audit on the provided DataFrame.

    This function acts as a safety gate to ensure the dataset contains the 
    mandatory features and maintains a minimum quality standard before 
    proceeding to the normalization phase.

    Args:
        df (pd.DataFrame): The unified dataset containing raw logs from 
            both synthetic attacks and real system traffic.

    Returns:
        bool: True if the dataset meets the structural requirements 
            (required columns present), False otherwise.
    """
    print("\n--- [PHASE 1: AUDITING DATA] ---")
    
    # Define minimum required columns
    required_cols = ['Process Time', 'Is Anomaly']

    # List of data with missing columns
    missing = [col for col in required_cols if col not in df.columns]

    # If missing list has data, stop process and return False
    if missing:
        print(f"[CRITICAL] Missing required columns: {missing}")
        return False

    # Get logs with null values
    null_counts = df.isnull().sum()

    # Print if there are null values
    if null_counts.any():
        print(f"[ALERT] Found null values:\n{null_counts[null_counts > 0]}")
        df.dropna(subset=['Log Level', 'Risk Score', 'Is Anomaly', 'Timestamp', 'Process Time'], inplace=True)
    else:
        print("[OK] There's no null values.")

    # Print total count of logs and return True
    print(f"[INFO] Total logs to process: {len(df)}")
    return True

def clean_and_normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply data transformation and feature normalization rules.

    This function standardizes the dataset by aligning temporal scales, 
    enforcing numerical precision, and unifying categorical text formats. 
    It ensures that the final dataset is consistent for feature encoding.

    Args:
        df (pd.DataFrame): The audited DataFrame from Phase 1.

    Returns:
        pd.DataFrame: A cleaned and normalized DataFrame with consistent 
            scaling and without redundant records.
    """
    print("\n--- [PHASE 2: Cleaning and Normalization] ---")

    # If a process_time is > 150, we assume it was injected as ms and convert it to seconds.
    df['Process Time'] = df['Process Time'].apply(lambda x: x/1000 if x > 150 else x)
    
    # Round process time to 2 digits
    df['Process Time'] = df['Process Time'].round(2)
    
    # Standardize text columna:
    # - Log Level
    if 'Log Level' in df.columns:
        df['Log Level'] = df['Log Level'].str.upper().str.strip()

    # - Service Name
    if 'Service Name' in df.columns:
        df['Service Name'] = df['Service Name'].str.lower().str.strip()

    # - Message
    if 'Message' in df.columns:
        df['Message'] = df['Message'].str.lower().str.strip()
    
    # Get logs count to report duplicate data
    initial_count = len(df)

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Print duplicate logs count
    print(f"[OK] Duplicates removed: {initial_count - len(df)}")
    
    # Return clean data
    return df

def main() -> None:
    """
    Orchestrate the end-to-end data cleansing workflow for the Sentinel dataset.

    This function serves as the entry point for the script. It manages the 
    loading of the unified 17k+ log dataset, triggers the quality audit 
    (Phase 1), executes the normalization logic (Phase 2), and exports the 
    final, high-fidelity CSV for machine learning model training.
    """

    # Define file paths
    input_path = "..\\..\\data\\raw\\sentinel_logs_final_dataset.csv" 
    output_path = "..\\..\\data\\processed\\sentinel_cleansed_v1.csv"

    # Ensure output path exists
    processed_dir = os.path.dirname(output_path)

    # Create path if doesn't exist
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
        print(f"[INFO] Created missing directory: {processed_dir}")
    
    try:
        # Read CSv
        df = pd.read_csv(input_path)
        print(f"[OK] Dataset loaded: {len(df)} logs found.")

    # Exception if there's no file
    except FileNotFoundError:
        print(f"[ERROR] File not found at: {input_path}")
        return 
    
    # Check there's no null values
    if check_data_quality(df):

        # Clean and normalize dataset
        df_cleaned = clean_and_normalize(df)
        
        # Save file
        df_cleaned.to_csv(output_path, index=False)
        print(f"\n[OK] Dataset with length {len(df_cleaned)} saved at path: {output_path}")

# Execute script
if __name__ == "__main__":
    main()