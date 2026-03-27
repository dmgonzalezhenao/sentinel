"""
Sentinel API Database Models Module

This module centralizes the domain entities for the Sentinel AIOps ecosystem.
It follows a modular architecture to ensure scalability and maintainability.

Architecture: Multi-tenant Log Aggregator.
Engine: PostgreSQL (Neon) via SQLAlchemy ORM.

Relationships:
- Organization (1) <---> (N) Users (Admin, Viewer, Service)
- Organization (1) <---> (N) Logs (Enforced Isolation)
- User (1) <---> (N) Logs (Authorship traceability)
- Log (1) <---> (N) AIAnalysis (Model inference results)
- AIAnalysis (1) <---> (1) Alert (Incident escalation)
- User (Analyst) (1) <---> (N) Alert (Assignment & Resolution)

Table: logs (Telemetry Data)
------------------------------------------------------------------------------
| Column          | Type           | Note                                    |
|-----------------|----------------|-----------------------------------------|
| id              | Integer        | PK, Autoincrement                       |
| service_name    | String         | Indexed, e.g. 'web-app'                 |
| log_level       | String         | INFO, ERROR, etc.                       |
| message         | String         | Main description                        |
| log_metadata    | JSONB          | Flexible software-specific              |
| timestamp       | DateTime       | Server default now time                 |
| user_id         | Integer        | FK -> users(id), Indexed                |
| organization_id | Integer        | FK -> organizations(id), Indexed         |
| process_time    | Float          | Observability latency (Middleware)      |
------------------------------------------------------------------------------

Table: ai_analyses (Intelligence Layer)
------------------------------------------------------------------------------
| Column            | Type           | Note                                  |
|-------------------|----------------|---------------------------------------|
| id                | Integer        | PK, Autoincrement                     |
| log_id            | Integer        | FK -> logs(id), Indexed               |
| model_version     | String         | e.g. 'isolation-forest-v1'            |
| prediction_score  | Float          | Range [0.0, 1.0], CheckConstraint     |
| is_anomaly        | Boolean        | Binary classification flag            |
| inference_time_ms | Float          | Performance metric (Latency)          |
| analysis_details  | JSONB          | Model-specific reasoning (Optional)   |
| created_at        | DateTime       | Inference timestamp                   |
------------------------------------------------------------------------------

Table: alerts (Operational Layer)
------------------------------------------------------------------------------
| Column          | Type           | Note                                    |
|-----------------|----------------|-----------------------------------------|
| id              | Integer        | PK, Autoincrement                       |
| analysis_id     | Integer        | FK -> ai_analyses(id), Unique           |
| severity        | String         | LOW, MEDIUM, HIGH, CRITICAL             |
| status          | String         | PENDING, RESOLVED, FALSE_POSITIVE       |
| assigned_to     | Integer        | FK -> users(id), Nullable (Analyst)     |
| notes           | String         | Human-provided resolution context       |
| created_at      | DateTime       | Alert trigger timestamp                 |
| resolved_at     | DateTime       | Closure timestamp (Nullable)            |
------------------------------------------------------------------------------

Table: users
----------------------------------------------------------------------------
| Column          | Type      | Note                                       |
|-----------------|-----------|--------------------------------------------|
| id              | Integer   | PK, Autoincrement                          |
| username        | String    | Indexed, Unique, e.g. 'mariogon'           |
| email           | String    | Indexed, Unique, e.g. 'example@gmail.com   |
| hashed_password | String    | Hash value                                 |
| is_active       | Boolean   | Default=True                               |
| role            | String    | ADMIN, SERVICE and VIEWER                  |
| created_at      | DateTime  | Server default now time                    |
| updated_at      | DateTime  | Server default now time                    |
| organization_id | Integer   | FK -> organizations(id)                    |
----------------------------------------------------------------------------
 
Table: organizations
-----------------------------------------------------------------
| Column      | Type      | Note                                |
-----------------------------------------------------------------
| id          | Integer   | PK, Autoincrement                   |
| name        | String    | Indexed, Unique, e.g. "Acme Corp"   |
| slug        | String    | Indexed, Unique, eg.g "acme"        |
| is_active   | Boolean   | Default=True                        |
| created_at  | DateTime  | Server default now time             |
| updated_at  | DateTime  | Server default now time             |
-----------------------------------------------------------------
"""

from .log import Log
from .user import User
from .organization import Organization
from .ai_analysis import AIAnalysis
from .alerts import Alert

# Expose models
__all__ = ["Log", "User", "Organization", "AIAnalysis", "Alert"]