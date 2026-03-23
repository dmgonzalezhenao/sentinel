# Sentinel: AI-Powered Observability & AIOps Infrastructure

**Sentinel** es una plataforma de inteligencia operacional diseñada para la ingesta, clasificación y detección de anomalías en logs en tiempo real. Utiliza un pipeline asíncrono para transformar registros de texto plano en insights accionables mediante Machine Learning clásico y NLP.

## 🚀 Estado del Proyecto
**Fase 1: Ingestión Estándar (Completada)**: API robusta con validación Pydantic y persistencia en PostgreSQL (Neon).

**Fase 2: Observabilidad y Seguridad (Completada)**: Aislamiento de datos por organizaciones, roles (Admin/Viewer), JWT Authentication y monitoreo de performance vía Middleware.

**Fase 3: Inteligencia y MLOps (En progreso)**: Implementación de tareas en segundo plano para clasificación de logs mediante Random Forest y detección de picos con Isolation Forest.

## 📋 Documentación
Para una visión detallada de los objetivos y especificaciones técnicas, consulta:
* [Especificación de Requerimientos](./docs/requirements.md)

## 🛠️ Stack Tecnológico (Core & AI Pipeline)

Para este proyecto, he seleccionado un stack basado en la asincronía y el procesamiento eficiente de datos, permitiendo que la IA analice registros sin degradar la experiencia del usuario.

| Categoría | Tecnología | Logo | Propósito Estratégico |
| :--- | :--- | :---: | :--- |
| **High-Performance API** | **FastAPI** | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) | Framework diseñado para manejar alta concurrencia y baja latencia en la ingesta masiva de logs. |
| **Data Integrity** | **Pydantic V2** | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white) | Garantiza la limpieza de datos en la fuente, evitando que el "ruido" afecte el entrenamiento de la IA. |
| **Cloud Persistence** | **PostgreSQL (Neon)** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) | Almacenamiento relacional serverless con indexación optimizada para consultas analíticas masivas. |
| **ML Engine** | **Scikit-Learn** | ![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) | Implementación de modelos de clasificación (**Random Forest**) y detección de anomalías (**Isolation Forest**). |
| **NLP Processing** | **TF-IDF & NLP** | ![NLP](https://img.shields.io/badge/NLP-Natural_Language-blue?style=for-the-badge) | Transformación de mensajes de texto en vectores numéricos procesables por algoritmos de aprendizaje. |
| **Security & IAM** | **JWT & Bcrypt** | ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) | Arquitectura **Multi-tenant** que garantiza el aislamiento total de datos y modelos entre organizaciones. |

Este stack permite que Sentinel procese logs con una latencia promedio de < 5ms, delegando el análisis predictivo a hilos de ejecución secundarios para no comprometer la disponibilidad.

## 🧠 Arquitectura AIOps

Sentinel separa la Ingesta de la Inferencia para garantizar alta disponibilidad:

* **Ingestión:** El log llega, se valida y se guarda en PostgreSQL instantáneamente.

* **Enriquecimiento (Async):** Una tarea en segundo plano procesa el texto con NLP (TF-IDF).

* **Clasificación:** Un modelo Random Forest asigna una categoría y un Risk Score.

* **Detección:** Un proceso de batch analiza ventanas de tiempo buscando anomalías de volumen.

## 🗺️ Roadmap (Próximas Fases)

### Fase 3: Inteligencia Artificial y Análisis (v0.7.0)
* 🤖 **NLP Engine:** Clasificación automática de mensajes de error para identificar "Causas Raíz".

* 📉 **Anomaly Detection:** Identificación de comportamientos inusuales en la frecuencia de logs.

* 🔔 **Smart Alerts:** Notificaciones automáticas basadas en el Risk Score calculado por la IA.

* 📊 **Analytics Dashboard:** Visualización de métricas de salud y predicciones de modelos.

---
Desarrollado como un proyecto de portafolio para demostrar arquitectura limpia y observabilidad.

Daniel González - 2026
