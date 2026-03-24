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

Table: logs
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
| organization_id | Integer        | FK -> organizations(id), Indexed        |
| process_time    | Float          | Observability latency (Middleware)      |
| ai_category     | String         | AI Generated, Indexed, e.g. 'db-error'  |
| risk_score      | SmallInteger   | AI Generated, Indexed, range = [0, 100] |
| is_anomaly      | Boolean        | AI Generated, Indexed                   |
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

# Expose models
__all__ = ["Log", "User", "Organization"]