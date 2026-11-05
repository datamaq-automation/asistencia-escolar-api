from flask import Blueprint, jsonify, request

from src.application.asistencia_escolar.dtos.accion_dto import (
    HistorialAccionesResponse,
    RegistrarAccionRequest,
)
from src.infrastructure.flask.dependencies import get_historial_uc, get_registrar_accion_uc
from src.infrastructure.sqlalchemy.database import SessionLocal

bp = Blueprint("acciones", __name__)


@bp.post("/acciones")
def registrar_accion():
    payload = request.get_json(silent=True) or {}
    dto = RegistrarAccionRequest.model_validate(payload)

    with SessionLocal() as session:
        use_case = get_registrar_accion_uc(session)
        respuesta = use_case.execute(dto)

    return jsonify(respuesta.model_dump(mode="json")), 201


@bp.get("/alumnos/<int:alumno_id>/acciones")
def historial_de_acciones(alumno_id: int):
    with SessionLocal() as session:
        use_case = get_historial_uc(session)
        respuesta = use_case.execute(alumno_id)

    return jsonify(respuesta.model_dump(mode="json"))
