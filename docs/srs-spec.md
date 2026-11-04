# SRS-SPECS: Sistema de Asistencia Escolar

> **Documento:** docs/srs-spec.md
> **Versión:** 1.0.0
> **Estado:** En revisión
> **Fecha:** Septiembre de 2026
> **Autora:** [D´addona María Gimena]
> **Contexto:** Proyecto integrador individual, [I.S.F.T N° 199]
> **Repositorio:** gimenadaddona/asistencia-escolar-api

---

## 1. Contexto estratégico y propuesta de valor

### 1.1. Foco y alcance

- **Mercado objetivo:** escuelas primarias de gestión estatal de la provincia de Buenos Aires.
- **Decisor (equipo directivo):** director/a y vicedirector/a, responsables de la trayectoria escolar y del seguimiento de la asistencia.
- **Usuarios:** docentes de grado, que registran asistencia y acciones desde celular o tablet; equipo de orientación y equipo directivo, que consultan el seguimiento.
- **Modalidad:** una institución por instalación, desplegada como **web local** en una computadora de la escuela y accedida por la red WiFi interna. Alternativa: servidor en la nube.
- **Fuera de alcance en esta versión:** calificaciones y boletines, liquidación de haberes, envío automático de mensajes a las familias (el sistema registra que la acción se realizó, no la envía), gestión de varias escuelas, integración con sistemas oficiales de la Dirección General de Cultura y Educación (a consultar con la inspección).

### 1.2. Pilares de valor

| Pilar | Implementación en este sistema |
|---|---|
| **Activos y entorno operativo** | Celulares y tablets de los docentes, una computadora de la escuela como servidor y la red WiFi interna. No requiere hardware especial. |
| **Software y lógica de negocio** | API REST con FastAPI. Las reglas de asistencia viven en la capa de dominio y los datos se guardan en SQLite. |
| **Impacto institucional** | Reduce el tiempo para detectar inasistencias reiteradas y deja registro de las acciones realizadas, para que directivo y orientación continúen el seguimiento sin repetir pasos. |

### 1.3. Roles, normativa y seguridad

- **Responsable técnica:** la autora del proyecto.
- **Ventanas operativas:** horario escolar de ambos turnos (mañana y tarde). El mantenimiento se hace fuera de ese horario.
- **Normativa:** el sistema trata datos de menores de edad, alcanzados por la Ley 25.326 de Protección de Datos Personales. Antes de un uso real se requiere autorización del equipo directivo y de la inspección, y es obligatorio incorporar autenticación (ver FR-10).

---

## 2. Modelo de negocio (Canvas adaptado)

Es una herramienta institucional para una escuela pública, sin fines comerciales. El Canvas se completó con ese criterio.

| Bloque | Definición |
|---|---|
| **Socios clave** | Equipo directivo y de orientación de la escuela; inspección; referente técnico que mantenga el servidor local. |
| **Actividades clave** | Pasar lista, detectar alertas, registrar acciones de seguimiento y consultar el historial. |
| **Recursos clave** | Reglas de negocio implementadas, base de datos de alumnos y computadora de la escuela. |
| **Propuesta de valor** | Detectar a tiempo la inasistencia reiterada y dar continuidad al seguimiento entre docente, orientación y directivo. |
| **Relación con usuarios** | Uso diario del docente; consulta periódica de directivo y orientación. |
| **Canales** | Web responsive por WiFi interno (prevista) y API REST con documentación en `/docs`. |
| **Segmentos** | Docentes, equipo directivo y equipo de orientación. |
| **Estructura de costos** | Sin licencias: tecnologías de código abierto. Costo de mantenimiento y respaldo de datos. |
| **Fuentes de ingresos** | No aplica. |

**Gobernanza de agentes IA:** desarrollo individual asistido por un asistente de IA (Claude). El detalle está en la sección "Uso de inteligencia artificial" del README.

**Escalera de evolución:**

1. **Hecho:** API con reglas de asistencia, alertas y seguimiento.
2. **Próximo:** interfaz web para celular y tablet, con login por rol y carga masiva de nómina.
3. **Futuro:** notificaciones, exportación de reportes y varias instituciones.

---

## 3. Requisitos de software

### 3.1. Requisitos funcionales

| ID | Requisito | Estado |
|---|---|---|
| FR-01 | **Registrar alumnos**, validando ciclo, grado y división. Se rechaza un grado que no corresponde al ciclo (Ciclo 1: 1° a 3°, Ciclo 2: 4° a 6°). | Implementado |
| FR-02 | **Listar la nómina**, con filtro opcional por grado y división. | Implementado |
| FR-03 | **Pasar lista** por división y fecha. Si el alumno está ausente, el motivo es obligatorio: climático, justificado o injustificado. Se valida que cada alumno exista, que pertenezca al grado y la división indicados, que no esté repetido en la planilla y que no tenga ya asistencia ese día. Si una validación falla, no se guarda ningún registro de la planilla. | Implementado |
| FR-04 | **Reporte de alertas:** lista los alumnos con N o más faltas injustificadas. Las faltas climáticas y las justificadas no cuentan. | Implementado |
| FR-05 | **Registrar acciones de seguimiento** (llamado a la familia, nota, reunión, derivación a orientación u otra), con descripción, autor, rol y fecha automática. | Implementado |
| FR-06 | **Consultar el historial de acciones** de un alumno. | Implementado |
| FR-07 | **Reporte de seguimiento** para directivo y orientación: cada alumno en alerta junto con todas las acciones que ya realizó el docente. | Implementado |
| FR-08 | **Carga masiva de nómina** en un solo pedido. | Pendiente |
| FR-09 | **Opciones para selectores en cascada** (ciclo, grado, división) que alimenten la interfaz. | Pendiente |
| FR-10 | **Autenticación y roles:** el docente carga datos; directivo y orientación solo consultan. **Obligatorio antes de un uso real.** | Pendiente |
| FR-11 | **Interfaz web responsive** para celular y tablet: elegir el curso con botones, ver a todos como presentes y marcar solo a quienes faltan. | Pendiente |

### 3.2. Requisitos no funcionales

Los valores de rendimiento son **objetivos**: todavía no se midieron.

| ID | Requisito |
|---|---|
| NFR-01 | **Rendimiento:** las consultas deberían responder en menos de 500 ms para una escuela de hasta unos 600 alumnos (objetivo a verificar). |
| NFR-02 | **Concurrencia:** debe soportar a varios docentes pasando lista a la vez. SQLite alcanza para una sola institución (objetivo a verificar). |
| NFR-03 | **Disponibilidad:** al ser web local, depende de que la computadora esté encendida en horario escolar. Se requieren copias de respaldo periódicas del archivo de la base de datos. |
| NFR-04 | **Seguridad:** datos de menores. Los secretos se manejan con variables de entorno y el archivo `.env` no se versiona. En producción hay que cambiar la `SECRET_KEY` por defecto. El login está pendiente. |
| NFR-05 | **Mantenibilidad:** las dependencias apuntan hacia adentro y el dominio no usa frameworks. Los tests automáticos de arquitectura están pendientes. |
| NFR-06 | **Usabilidad:** pensada para uso táctil y con la menor cantidad de toques posible. Se implementa con la interfaz web. |
| NFR-07 | **Portabilidad:** Windows con Python 3.10 o superior (desarrollado con 3.13). |

---

## 4. Stack y arquitectura

### 4.1. Stack tecnológico

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.13 (3.10 o superior) |
| Arquitectura | Clean Architecture con Screaming DDD |
| Framework web | FastAPI, servido con Uvicorn |
| Validación | Pydantic v2 |
| Configuración | pydantic-settings, con variables de entorno |
| Persistencia | SQLAlchemy 2 **síncrono** sobre SQLite |
| Pruebas | pytest |
| Linters y tipado | ruff y pyright (pendientes de ejecutar) |

La plantilla sugiere SQLAlchemy asíncrono. Se eligió el modo síncrono porque todos los casos de uso son síncronos y, para una sola escuela con SQLite, no aporta ventaja. Podría migrarse más adelante.

### 4.2. Estructura del proyecto

```
src/
├── domain/asistencia_escolar/
│   ├── entities.py          # Alumno, RegistroAsistencia, AccionSeguimiento
│   ├── value_objects.py     # Ciclo, AnioEscolar, Division, MotivoInasistencia, ...
│   ├── services.py          # ServicioDeteccionAlertaInasistencia
│   ├── repositories.py      # Interfaces abstractas
│   ├── events.py            # AlertaInasistenciaGenerada
│   └── exceptions.py
├── application/asistencia_escolar/
│   ├── use_cases/           # 7 casos de uso
│   ├── dtos/                # Request y Response (Pydantic)
│   └── mappers/             # DTO <-> entidad
├── infrastructure/
│   ├── fastapi/             # routers/ y dependencies.py
│   ├── sqlalchemy/          # database.py, models/, repositories/
│   └── settings/            # config.py y logger.py
└── main.py
tests/
├── unit/                    # Dominio y casos de uso con repositorios en memoria
└── integration/             # Repositorios contra SQLite en memoria
```

### 4.3. Modelo de datos

| Tabla | Campos principales |
|---|---|
| `alumnos` | id, nombre, apellido, ciclo, anio, division |
| `asistencias` | id, alumno_id, fecha, estado, motivo_inasistencia. Restricción única sobre (alumno_id, fecha). |
| `acciones` | id, alumno_id, fecha, tipo_accion, descripcion, realizado_por, rol_autor |

### 4.4. Casos de uso y endpoints

| Caso de uso | Endpoint |
|---|---|
| Registrar alumno | `POST /api/v1/alumnos` |
| Listar nómina | `GET /api/v1/alumnos` |
| Pasar lista | `POST /api/v1/asistencia` |
| Registrar acción de seguimiento | `POST /api/v1/acciones` |
| Consultar historial de acciones | `GET /api/v1/alumnos/{id}/acciones` |
| Generar reporte de alertas | `GET /api/v1/reportes/alertas?limite=N` |
| Generar reporte de seguimiento | `GET /api/v1/reportes/seguimiento?limite=N` |

### 4.5. Reglas de arquitectura de la plantilla

| Regla | Estado |
|---|---|
| Dependencia de capas | Respetada en el diseño. Falta la verificación automática. |
| Archivos `__init__.py` vacíos | Respetada. Falta la verificación automática. |
| Parámetros críticos desde configuración | **Parcial:** las listas de grados y divisiones y el umbral por defecto de alertas (5) están en el código. Conviene moverlos a configuración. |
| Controladores delgados | Respetada: los routers solo llaman a los casos de uso. La capa `adapters` no se usa por ahora. |
| Imports absolutos | Respetada. |
| Tipado estricto | **Parcial:** pyright todavía no se ejecutó, y el reporte de seguimiento usa `List[dict]` para las acciones, que debería ser un tipo definido. |

---

## 5. Calidad y pruebas

- **61 tests automáticos pasando:** 56 unitarios (dominio y casos de uso con repositorios en memoria) y 5 de integración (repositorios reales contra SQLite en memoria).
- **Verificación manual** de cada endpoint desde la documentación interactiva en `/docs`.
- **Defecto encontrado y corregido:** al probar manualmente, "pasar lista" aceptaba alumnos inexistentes y valores inválidos de grado y división. Se agregaron las validaciones y tests de regresión.
- **Pendiente:** ruff, pyright, tests de arquitectura y medición de cobertura.

Comandos de verificación:

```
python -m pytest -q
python -m uvicorn src.main:app --reload
```

---

## 6. Pendientes y hoja de ruta

| Pendiente | Prioridad |
|---|---|
| Login por usuario y rol (FR-10) | Alta: obligatorio antes de usar con datos reales |
| Autorización de la dirección y la inspección | Alta: antes de un uso real |
| Carga masiva de nómina y opciones en cascada (FR-08, FR-09) | Media |
| Interfaz web para celular y tablet (FR-11) | Media |
| ruff, pyright y tests de arquitectura | Media |
| Mover parámetros críticos a configuración y tipar el reporte de seguimiento | Baja |
| Despliegue local con IP fija y respaldo periódico de la base de datos | Al desplegar |
