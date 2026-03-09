# Especificación de Requerimientos - Project Sentinel

## 1. Objetivo del Proyecto
Desarrollar una infraestructura de observabilidad "AI-Ready" capaz de centralizar registros de eventos (logs) de múltiples servicios, garantizando la integridad de los datos y preparando el terreno para análisis predictivos.

## 2. Requerimientos Funcionales (RF)

| ID | Requerimiento | Descripción | Estado |
| :--- | :--- | :--- | :--- |
| **RF-01** | Ingesta de Logs | Endpoint para recibir paquetes de datos en formato JSON de múltiples servicios. | ✅ |
| **RF-02** | Validación Estricta | Rechazo de logs que no cumplan con el esquema definido (Timestamp, Level, etc.). | ✅ |
| **RF-03** | Persistencia | Almacenamiento de eventos validados en base de datos PostgreSQL. | ✅ |
| **RF-04** | Gestión de Metadata | Soporte para información contextual flexible mediante campos JSONB. | ✅ |
| **RF-05** | Normalización | Limpieza y estandarización de logs antes del almacenamiento. | ✅ |
| **RF-06** | Consulta con Filtros | Endpoint GET para buscar logs por servicio, nivel de severidad y rango de fechas. | ✅ |
| **RF-07** | Paginación de Datos | Implementación de límites y offsets para manejar grandes volúmenes de registros. | ✅ |
| **RF-08** | Monitoreo de Salud | El endpoint de salud debe verificar la conexión activa con la base de datos. | ✅ |

## 3. Requerimientos No Funcionales (RNF)

| ID | Requerimiento | Descripción | Estado |
| :--- | :--- | :--- | :--- |
| **RNF-01** | Asincronía | El procesamiento interno no debe bloquear la respuesta HTTP al cliente. | ✅ |
| **RNF-02** | Contenerización | Ejecución de todo el stack tecnológico mediante Docker Compose. | 🏗️ |
| **RNF-03** | Tipado Estricto | Implementación completa de Type Hints y Pydantic para robustez. | ✅ |
| **RNF-04** | Seguridad de Acceso | Validación de identidad mediante API Keys para servicios autorizados. | 🏗️ |

## 4. Definición del Contrato (Data Schema)

Cada log enviado debe seguir obligatoriamente esta estructura:

```json
{
  "service_name": "string",
  "log_level": "INFO | WARNING | ERROR | CRITICAL",
  "message": "string",
  "timestamp": "2026-02-27T15:30:00Z",
  "log_metadata": {
    "key": "value"
  }
}
```
