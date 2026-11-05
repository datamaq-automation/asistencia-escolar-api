from flask import Blueprint, jsonify, request

from src.application.asistencia_escolar.dtos.asistencia_dto import PasarListaRequest
from src.infrastructure.flask.dependencies import get_pasar_lista_uc
from src.infrastructure.sqlalchemy.database import SessionLocal

bp = Blueprint("asistencia", __name__)


@bp.post("/asistencia")
def pasar_lista():
    payload = request.get_json(silent=True) or {}
    dto = PasarListaRequest.model_validate(payload)

    with SessionLocal() as session:
        use_case = get_pasar_lista_uc(session)
        respuesta = use_case.execute(dto)

    return jsonify(respuesta.model_dump(mode="json")), 201
