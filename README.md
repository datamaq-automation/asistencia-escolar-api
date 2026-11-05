# Sistema de Asistencia Escolar

Proyecto integrador individual: API REST para el control de asistencia diaria en una escuela primaria, con nómina por ciclo, grado y división, alertas por inasistencias reiteradas y seguimiento de las acciones que realiza el equipo docente.

## ¿Qué problema resuelve?

Además de registrar presentes y ausentes, el sistema permite que el **docente**, el **equipo directivo** y el **equipo de orientación** compartan la misma información sobre cada alumno. Cuando un alumno acumula faltas injustificadas, el sistema lo detecta y muestra qué acciones ya realizó el docente (llamados a la familia, reuniones, notas), para que directivo y orientación continúen el seguimiento sin repetir pasos.

## Reglas de negocio

- Escuela primaria: **6 grados** (1° a 6°), en dos ciclos (Ciclo 1: 1° a 3°, Ciclo 2: 4° a 6°).
- **4 divisiones**: A y B (turno mañana), C y D (turno tarde).
- Toda ausencia tiene **uno de tres motivos**: climático, justificado o injustificado.
- **Solo las faltas injustificadas generan alertas.** Las climáticas y las justificadas no cuentan.
- No se puede pasar lista dos veces al mismo alumno el mismo día.
- Al pasar lista se valida que cada alumno exista y pertenezca al grado y la división indicados. Si algo falla, no se guarda nada de la planilla.
- Roles: docente (carga datos), directivo y orientación (consulta).

## Tecnologías

Python 3.13, Flask, SQLAlchemy 2 con SQLite, Pydantic v2 y pytest.

## Arquitectura

Clean Architecture con Screaming DDD. Cada capa solo depende de las capas internas: el dominio no conoce ni FastAPI ni la base de datos.

```
src/
├── domain/           # Entidades, value objects, servicio de alertas, interfaces de repositorios
├── application/      # 7 casos de uso, DTOs (Pydantic) y mappers
├── adapters/         # Capa reservada: por ahora los routers llaman directo a los casos de uso
├── infrastructure/
│   ├── flask/        # Routers y dependencias
│   ├── sqlalchemy/   # Modelos de tablas y repositorios reales
│   └── settings/     # Configuración y logging
└── main.py           # Punto de entrada de la API
tests/
├── unit/             # Tests de dominio y casos de uso (con repositorios en memoria)
└── integration/      # Tests de los repositorios contra una base SQLite en memoria
```

## Estado del proyecto

| Componente | Estado |
|---|---|
| Domain (entidades, reglas, servicio de alertas) | Completo |
| Application (7 casos de uso) | Completo |
| Infrastructure: base de datos SQLite y repositorios reales | Completo |
| API REST con Flask | Completa (primera versión) |
| Login por usuario y rol | Pendiente |
| Carga masiva de nómina | Pendiente |
| Interfaz web para celular y tablet | Pendiente |
| Controles de calidad (ruff, pyright, tests de arquitectura) | Pendiente |

**Tests:** 61 pasando (56 unitarios y 5 de integración).

## API

Con el servidor corriendo, la API queda disponible en `http://127.0.0.1:5000`.

| Método | Ruta | Qué hace |
|---|---|---|
| POST | `/api/v1/alumnos` | Registra un alumno |
| GET | `/api/v1/alumnos` | Lista la nómina (filtros opcionales `anio` y `division`) |
| POST | `/api/v1/asistencia` | Pasa lista de una división en una fecha |
| POST | `/api/v1/acciones` | Registra una acción de seguimiento |
| GET | `/api/v1/alumnos/{id}/acciones` | Historial de acciones de un alumno |
| GET | `/api/v1/reportes/alertas?limite=N` | Alumnos con N o más faltas injustificadas |
| GET | `/api/v1/reportes/seguimiento?limite=N` | Alertas junto con las acciones ya realizadas |

### Valores permitidos

- `ciclo`: `"1"` o `"2"`
- `anio`: `"1°"` a `"6°"`
- `division`: `"A"`, `"B"`, `"C"` o `"D"`
- `motivo_inasistencia` (obligatorio si `presente` es `false`): `climatico`, `justificado` o `injustificado`
- `tipo_accion`: `llamado_familia`, `nota_cuaderno`, `reunion_familia`, `derivacion_orientacion` u `otro`
- `rol_autor`: `docente`, `directivo` u `orientacion`

## Instalación y uso (Windows, PowerShell)

Requisitos: Python 3.10 o superior (desarrollado con 3.13) y Git.

```powershell
git clone https://github.com/gimenadaddona/asistencia-escolar-api.git
cd asistencia-escolar-api
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Levantar la API (la base de datos `asistencia_escolar.db` se crea sola):

```powershell
python -m flask --app src.main run --debug
```

Ejecutar los tests:

```powershell
python -m pytest -q
```

## Despliegue previsto

Pensado para correr como **web local** en una computadora de la escuela, accesible desde celulares y tablets por la red WiFi interna. No depende de internet y los datos de los alumnos quedan dentro de la institución.

## Seguridad y datos personales

El sistema maneja datos de menores de edad, alcanzados por la Ley 25.326 de Protección de Datos Personales. Antes de un uso real es obligatorio incorporar autenticación por usuario y rol. **Nunca se deben subir datos reales de alumnos ni archivos `.env` al repositorio.**

## Autora

Proyecto integrador individual con asistencia guiada de Claude IA.
