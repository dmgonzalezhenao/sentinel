# Sentinel: AI-Ready Observability Infrastructure

**Sentinel** es una infraestructura de backend para la ingesta, procesamiento y análisis de logs en tiempo real. Este proyecto está diseñado para centralizar registros de múltiples microservicios y preparar los datos para futuros modelos de Inteligencia Artificial.

## 🚀 Estado del Proyecto
**Fase 1: Ingestión Estándar (Completada)**: API funcional con validación mediante Pydantic y persistencia en PostgreSQL (Neon).

**Fase 2: Observabilidad y Seguridad (En desarrollo)**: Implementación de filtrado avanzado, paginación y control de acceso mediante API Keys.

## 📋 Documentación
Para una visión detallada de los objetivos y especificaciones técnicas, consulta:
* [Especificación de Requerimientos](./docs/REQUIREMENTS.md)

## 🛠️ Stack Tecnológico (Estado Actual)

| Tecnología | Logo | Versión | Propósito y Aplicación |
| :--- | :---: | :--- | :--- |
| **FastAPI** | <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="80"> | `0.113.0` | **Core del Framework:** Manejo de peticiones asíncronas (`async/await`) para alta concurrencia sin bloqueo de hilos. |
| **Pydantic V2** | <img src="https://docs.pydantic.dev/latest/img/logo-white.svg" width="40" style="background-color: #e92063; padding: 5px; border-radius: 3px;"> | `2.11.7+` | **Validación y Tipado:** Garantiza la integridad de los datos entrantes mediante esquemas estrictos y serialización rápida. |
| **SQLAlchemy** | <img src="https://www.sqlalchemy.org/img/sqla_logo.png" width="80"> | `2.0.32` | **ORM:** Gestión de la base de datos mediante programación orientada a objetos y mapeo declarativo avanzado. |
| **PostgreSQL** | <img src="https://www.postgresql.org/media/img/about/press/elephant.png" width="40"> | `v16+` | **Persistencia:** Almacenamiento relacional robusto hospedado en la nube a través de **Neon.tech**. |
| **Psycopg2** | <img src="https://pypi.org/static/images/logo-small.95988418.svg" width="40"> | `2.9.9` | **Database Driver:** Puente de comunicación de bajo nivel entre la aplicación Python y el motor de PostgreSQL. |
| **Python-Dotenv**| <img src="https://raw.githubusercontent.com/motdotla/dotenv/master/dotenv.png" width="40"> | `1.0.1` | **Seguridad:** Gestión de variables de entorno para proteger credenciales sensibles (DB URLs, API Keys). |



## 🗺️ Roadmap (Próximas Fases)

### **Fase 2: Observabilidad y Seguridad (En Progreso)**
* 🐳 **Docker & Docker Compose:** Contenerización de la API y la base de datos para asegurar la portabilidad del entorno de desarrollo.
* 🔑 **API Key Authentication:** Implementación de seguridad en los encabezados HTTP para restringir el acceso solo a servicios autorizados.
* 📊 **Paginación y Filtros:** Optimización de consultas `GET` para manejar grandes volúmenes de logs sin saturar la memoria del servidor.

### **Fase 3: Inteligencia Artificial y Análisis**
* 🧠 **Detección de Anomalías:** Integración de modelos de Machine Learning para identificar comportamientos inusuales en tiempo real.
* 🏷️ **Clasificación Automática:** Uso de procesamiento de lenguaje natural (NLP) para categorizar logs no estructurados y mejorar la búsqueda.
---
Desarrollado como un proyecto de portafolio para demostrar arquitectura limpia y observabilidad.

Daniel González - 2026