# Documentación de la Base de Datos: Proyecto Sentinel
Este documento describe la capa de persistencia de Sentinel, utilizando **Neon (PostgreSQL)** y **SQLAlchemy** como ORM.

## Arquitectura
Utilizamos un enfoque de **Mapeo Declarativo**. La clase Base (generada mediante declarative_base) actúa como un registro centralizado para todos los modelos. Esto evita importaciones circulares y asegura que todos los modelos compartan el mismo motor de conexión (engine).

## Entidad: logs
Esta es la tabla principal donde se registran todos los eventos enviados por los servicios externos.

### Estructura de la Tabla: `logs`

| Columna | Tipo | Atributos | Descripción |
| :--- | :--- | :--- | :--- |
| **id** | `Integer` | PK, Auto-inc | Identificador único del log. |
| **service_name** | `String(50)` | Indexed | Nombre de la app (ej. 'frontend-api'). |
| **log_level** | `String(20)` | Not Null | Nivel (INFO, ERROR, etc.). |
| **message** | `Text` | Not Null | Descripción del evento. |
| **metadata** | `JSONB` | Nullable | Datos extra en formato JSON. |
| **timestamp** | `DateTime` | Default: now() | Fecha y hora con zona horaria (UTC). |

## Decisiones Técnicas
### 1. ¿Por qué JSONB para metadata?
A diferencia del tipo JSON estándar, el JSONB (JSON Binario) se almacena en un formato descompuesto.

**Beneficio**: Soporta indexación y es mucho más rápido de procesar. Esto nos permite hacer consultas sobre claves específicas dentro de los logs sin tener que escanear toda la tabla.

### 2. Timestamps con Zona Horaria
Todas las marcas de tiempo se almacenan con información de zona horaria UTC. Esto evita problemas de sincronización cuando los logs provienen de servidores ubicados en diferentes regiones geográficas.

### 3. Indexación Estratégica
La columna service_name está indexada porque es el filtro más frecuente que utilizaremos al depurar aplicaciones específicas.