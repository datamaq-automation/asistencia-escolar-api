from sqlalchemy.orm import Session

from src.application.asistencia_escolar.use_cases.consultar_historial_acciones import (
    ConsultarHistorialAccionesUseCase,
)
from src.application.asistencia_escolar.use_cases.generar_reporte_alertas import (
    GenerarReporteAlertasUseCase,
)
from src.application.asistencia_escolar.use_cases.generar_reporte_seguimiento import (
    GenerarReporteSeguimientoUseCase,
)
from src.application.asistencia_escolar.use_cases.listar_nomina import ListarNominaUseCase
from src.application.asistencia_escolar.use_cases.pasar_lista_asistencia import (
    PasarListaAsistenciaUseCase,
)
from src.application.asistencia_escolar.use_cases.registrar_accion_seguimiento import (
    RegistrarAccionSeguimientoUseCase,
)
from src.application.asistencia_escolar.use_cases.registrar_alumno import (
    RegistrarAlumnoUseCase,
)
from src.domain.asistencia_escolar.services import ServicioDeteccionAlertaInasistencia
from src.infrastructure.sqlalchemy.repositories.accion_repository import (
    SqlAlchemyAccionSeguimientoRepository,
)
from src.infrastructure.sqlalchemy.repositories.alumno_repository import (
    SqlAlchemyAlumnoRepository,
)
from src.infrastructure.sqlalchemy.repositories.asistencia_repository import (
    SqlAlchemyAsistenciaRepository,
)


def get_registrar_alumno_uc(session: Session) -> RegistrarAlumnoUseCase:
    return RegistrarAlumnoUseCase(alumno_repository=SqlAlchemyAlumnoRepository(session))


def get_listar_nomina_uc(session: Session) -> ListarNominaUseCase:
    return ListarNominaUseCase(alumno_repository=SqlAlchemyAlumnoRepository(session))


def get_pasar_lista_uc(session: Session) -> PasarListaAsistenciaUseCase:
    return PasarListaAsistenciaUseCase(
        asistencia_repository=SqlAlchemyAsistenciaRepository(session),
        alumno_repository=SqlAlchemyAlumnoRepository(session),
    )


def get_registrar_accion_uc(session: Session) -> RegistrarAccionSeguimientoUseCase:
    return RegistrarAccionSeguimientoUseCase(
        accion_repository=SqlAlchemyAccionSeguimientoRepository(session)
    )


def get_historial_uc(session: Session) -> ConsultarHistorialAccionesUseCase:
    return ConsultarHistorialAccionesUseCase(
        accion_repository=SqlAlchemyAccionSeguimientoRepository(session),
        alumno_repository=SqlAlchemyAlumnoRepository(session),
    )


def get_reporte_alertas_uc(session: Session) -> GenerarReporteAlertasUseCase:
    return GenerarReporteAlertasUseCase(
        alumno_repository=SqlAlchemyAlumnoRepository(session),
        asistencia_repository=SqlAlchemyAsistenciaRepository(session),
        servicio_alertas=ServicioDeteccionAlertaInasistencia(),
    )


def get_reporte_seguimiento_uc(session: Session) -> GenerarReporteSeguimientoUseCase:
    alumno_repo = SqlAlchemyAlumnoRepository(session)
    return GenerarReporteSeguimientoUseCase(
        reporte_alertas_use_case=GenerarReporteAlertasUseCase(
            alumno_repository=alumno_repo,
            asistencia_repository=SqlAlchemyAsistenciaRepository(session),
            servicio_alertas=ServicioDeteccionAlertaInasistencia(),
        ),
        accion_repository=SqlAlchemyAccionSeguimientoRepository(session),
        alumno_repository=alumno_repo,
    )
