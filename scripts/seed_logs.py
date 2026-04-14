"""
Synthetic log generator for Machine Learning training.

This module generates and injects 10,000 synthetic log entries into the 
database to serve as a baseline dataset for training anomaly detection models.
"""
import asyncio
import httpx
import random
import time
from datetime import datetime, timedelta, timezone
from typing import TypedDict, List

# 1. Configuration constants for the simulation
API_BASE_URL = "http://127.0.0.1:8000/api/v1"
TOTAL_LOGS = 10000
CONCURRENCY_LIMIT = 10  # Cambie a 25 porque tengo entendido que Postgre no permite màs de 30 o no se si era Neon
ANOMALY_RATE = 0.05      # 5% of logs will be random anomalies

# 2. Hardcoded service credentials provided for the simulation
# These correspond to the IDs assigned in the database
SERVICE_CREDENTIALS = [
    # Unicatólica
    {"username": "svc.auth.campus@unicatolica.edu.co", "password": "kP9!zR2$mV7*nQ5x"},
    {"username": "svc.grades.engine@unicatolica.edu.co", "password": "bH4@sT9^jL1#wX8y"},
    {"username": "svc.moodle.api@unicatolica.edu.co", "password": "gF7&dK2*pN5!vM9q"},
    
    # Logitech
    {"username": "gps.tracker@logitech-cali.com", "password": "mN5*vB2!xZ9#kQ7w"},
    {"username": "fleet.mgmt@logitech-cali.com", "password": "pL1$rT4@jH7^nY2x"},
    {"username": "route.opt@logitech-cali.com", "password": "vX9&mK3*dQ5!sR8p"},
    
    # Finanzas Seguras
    {"username": "pay.gateway@finanzas-seguras.co", "password": "hG7#dF2$sS9*kL1v"},
    {"username": "user.wallet@finanzas-seguras.co", "password": "qW4@rT8^pM3!nX5z"},
    {"username": "fraud.det@finanzas-seguras.co", "password": "bV9&mK2*dQ7#sR4p"}
]

# 3. Manual mapping: Associates each username with its exact service_name in the DB
SERVICE_NAME_MAP = {
    "svc.auth.campus@unicatolica.edu.co": "Campus-Auth",
    "svc.grades.engine@unicatolica.edu.co": "Grades-Engine",
    "svc.moodle.api@unicatolica.edu.co": "Moodle-API",
    "gps.tracker@logitech-cali.com": "GPS-Tracker",
    "fleet.mgmt@logitech-cali.com": "Fleet-Management",
    "route.opt@logitech-cali.com": "Route-Optimization",
    "pay.gateway@finanzas-seguras.co": "Payment-Gateway",
    "user.wallet@finanzas-seguras.co": "User-Wallet",
    "fraud.det@finanzas-seguras.co": "Fraud-Detection"
}

# 1. Define the structure for the authenticated service object
class ServiceAuth(TypedDict):
    token: str
    service_name: str

async def authenticate_services() -> List[ServiceAuth]:
    """
    Authenticates all service accounts and retrieves their JWT access tokens.
    Returns a list of ServiceAuth dictionaries.
    """
    authenticated_services: List[ServiceAuth] = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for creds in SERVICE_CREDENTIALS:
            try:
                response = await client.post(
                    f"{API_BASE_URL}/auth/login",
                    data={"username": creds["username"], "password": creds["password"]}
                )
                response.raise_for_status() 
                
                token = response.json().get("access_token")
                target_service_name = SERVICE_NAME_MAP.get(creds["username"], "Unknown-Service")
                
                # We explicitly create the dictionary matching the TypedDict
                auth_entry: ServiceAuth = {
                    "token": str(token),
                    "service_name": str(target_service_name)
                }
                authenticated_services.append(auth_entry)
                print(f"[AUTH] Successfully authenticated: {creds['username']}")
                
            except httpx.HTTPStatusError as e:
                print(f"[ERROR] Authentication failed: {e.response.text}")
                
    return authenticated_services

def generate_log_payload(service_name: str) -> dict:
    """
    Generates a realistic log payload with randomized timestamps and injected anomalies.
    Requires the corresponding service_name to maintain relational integrity in the DB.
    """
    days_ago = random.uniform(0, 30)
    simulated_time = datetime.now(timezone.utc) - timedelta(days=days_ago)
    is_anomaly = random.random() < ANOMALY_RATE
    
    if is_anomaly:
        log_level = random.choice(["ERROR", "CRITICAL"])
        message = random.choice([
            "Database connection timeout detected",
            "Multiple failed payment attempts recorded",
            "Unexpected memory overflow in processing queue",
            "Unauthorized access attempt blocked by firewall"
        ])
        log_metadata = {
            "risk_score": random.randint(85, 100),
            "cpu_spike": f"{random.randint(90, 100)}%",
            "is_anomaly": True
        }
    else:
        log_level = random.choice(["INFO", "DEBUG"])
        message = random.choice([
            "User session validated successfully",
            "Data synchronization completed without errors",
            "Ping received from remote server",
            "Cache updated successfully"
        ])
        log_metadata = {
            "risk_score": random.randint(0, 20),
            "cpu_spike": f"{random.randint(10, 40)}%",
            "is_anomaly": False
        }

    return {
        "service_name": service_name,
        "log_level": log_level,
        "message": message,
        "log_metadata": log_metadata,
        "timestamp": simulated_time.isoformat() 
    }

async def send_single_log(client: httpx.AsyncClient, token: str, payload: dict, semaphore: asyncio.Semaphore) -> int:
    """
    Sends a single HTTP POST request to the API while respecting the concurrency limit.
    """
    async with semaphore:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = await client.post(
                f"{API_BASE_URL}/logs/",
                json=payload,
                headers=headers
            )
            return response.status_code
        except Exception as e:
            return 500

async def main():
    """
    Main execution pipeline: Authentication -> Payload Generation -> Concurrent Ingestion.
    """
    print("--- Starting Sentinel Multi-Tenant Log Simulation ---")
    
    # Step 1: Get tokens and service names
    services_data = await authenticate_services()
    if not services_data:
        print("[FATAL] No tokens retrieved. Check your database or API status.")
        return

    print(f"\n[INFO] Starting concurrent ingestion of {TOTAL_LOGS} logs...")
    
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    tasks = []
    start_time = time.perf_counter()
    
    """Put connections limit"""
    limits = httpx.Limits(max_keepalive_connections=20, max_connections=50)

    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0), limits=limits) as client:
        for i in range(TOTAL_LOGS):
            # Now the linter knows exactly what fields random_service has
            random_service: ServiceAuth = random.choice(services_data)
            
            payload = generate_log_payload(random_service["service_name"])
            
            task = asyncio.create_task(
                send_single_log(client, random_service["token"], payload, semaphore)
            )
            tasks.append(task)

            """Print succesful messages"""
            if (i + 1) % 500 == 0:
                print(f"[PROGRESS] Queued {i + 1}/{TOTAL_LOGS} logs...")
            
        results = await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    total_time = end_time - start_time
    successful_requests = sum(1 for status in results if status in (200, 201))
    rps = TOTAL_LOGS / total_time

    print("\n--- Simulation Complete ---")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Throughput: {rps:.2f} Requests/Second")
    print(f"Successful Insertions: {successful_requests}/{TOTAL_LOGS}")

if __name__ == "__main__":
    asyncio.run(main())
