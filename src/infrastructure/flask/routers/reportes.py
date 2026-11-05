from flask import Blueprint, jsonify, request

from src.application.asistencia_escolar.dtos.asistencia_dto import (
    ReporteAlertasRequest,
)
from src.infrastructure.flask.dependencies import get_reporte_alertas_uc, get_reporte_seguimiento_uc
from src.infrastructure.sqlalchemy.database import SessionLocal

bp = Blueprint("reportes", __name__)


@bp.get("/reportes/alertas")
def reporte_alertas():
    limite = request.args.get("limite", default=5, type=int)
    dto = ReporteAlertasRequest(limite_faltas_injustificadas=limite)

    with SessionLocal() as session:
        use_case = get_reporte_alertas_uc(session)
        respuesta = use_case.execute(dto)

    return jsonify(respuesta.model_dump(mode="json"))


@bp.get("/reportes/seguimiento")
def reporte_seguimiento():
    limite = request.args.get("limite", default=5, type=int)
    dto = ReporteAlertasRequest(limite_faltas_injustificadas=limite)

    with SessionLocal() as session:
        use_case = get_reporte_seguimiento_uc(session)
        respuesta = use_case.execute(dto)

    return jsonify(respuesta.model_dump(mode="json"))
