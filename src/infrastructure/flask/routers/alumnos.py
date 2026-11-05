from typing import Optional

from flask import Blueprint, jsonify, request

from src.application.asistencia_escolar.dtos.alumno_dto import (
    ListarNominaRequest,
    RegistrarAlumnoRequest,
)
from src.infrastructure.flask.dependencies import get_listar_nomina_uc, get_registrar_alumno_uc
from src.infrastructure.sqlalchemy.database import SessionLocal

bp = Blueprint("alumnos", __name__)


@bp.post("/alumnos")
def registrar_alumno():
    payload = request.get_json(silent=True) or {}
    dto = RegistrarAlumnoRequest.model_validate(payload)

    with SessionLocal() as session:
        use_case = get_registrar_alumno_uc(session)
        respuesta = use_case.execute(dto)

    return jsonify(respuesta.model_dump(mode="json")), 201


@bp.get("/alumnos")
def listar_nomina():
    anio = request.args.get("anio")
    division = request.args.get("division")
    dto = ListarNominaRequest(anio=anio, division=division)

    with SessionLocal() as session:
        use_case = get_listar_nomina_uc(session)
        respuesta = use_case.execute(dto)

    return jsonify(respuesta.model_dump(mode="json"))
