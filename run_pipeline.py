"""
Sentinel Data Pipeline Orchestrator
Automates the end-to-end flow from raw log ingestion to ML-ready datasets.
"""

# Import sys to get pipeline files
import sys
import subprocess
from pathlib import Path

def run_script(script_name: str) -> bool:
    """Executes a python script and monitors its exit status."""
    print(f"\n>>> [EXECUTING: {script_name}] <<<")
    try:
        # Use subprocess to execute every script
        result = subprocess.run([sys.executable, script_name], check=True)

        # Return True if there's no errors
        return True
    
    # Exception if there's a subprocess error
    except subprocess.CalledProcessError as e:
        print(f"\n[CRITICAL ERROR] {script_name} failed with exit code {e.returncode}")
        return False

def main():
    # Define pipeline steps
    pipeline_steps = [
        "scripts/data_generation/01_brute_force.py",
        "scripts/data_generation/02_sql_injection.py", 
        "scripts/data_generation/03_data_reinforcement.py", 
        "scripts/data_generation/04_xss_injection.py", 
        "scripts/data_generation/05_data_exfiltration.py", 
        "scripts/data_cleansing/06_normalize_logs.py"
    ]

    # Print start message
    print("="*50)
    print("SENTINEL DATA PIPELINE - STARTING AUTOMATION")
    print("="*50)

    # Execute script step by step
    for step in pipeline_steps:
        # Check script exists
        if not Path(step).exists():
            print(f"[ERROR] Script not found: {step}")
            sys.exit(1)

        # If there's an execution error
        if not run_script(step):
            print("\n[STOPPED] Pipeline halted due to errors in the previous stage.")
            sys.exit(1)

    print("\n" + "="*50)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("Final dataset is ready in data/processed/")
    print("="*50)

# Run pipeline
if __name__ == "__main__":
    main()