from flask import Flask, jsonify, render_template
from pydantic import ValidationError

from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.infrastructure.flask.routers import acciones, alumnos, asistencia, reportes
from src.infrastructure.settings.config import get_settings
from src.infrastructure.sqlalchemy.database import engine
from src.infrastructure.sqlalchemy.models import orm_models


def create_app() -> Flask:
    settings = get_settings()
    orm_models.Base.metadata.create_all(engine)

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config["JSON_SORT_KEYS"] = False
    app.config["JSON_AS_ASCII"] = False

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(DatosInvalidosError)
    def manejar_datos_invalidos(exc: DatosInvalidosError):
        return jsonify({"detalle": str(exc)}), 400

    @app.errorhandler(ValueError)
    def manejar_valor_invalido(exc: ValueError):
        return jsonify({"detalle": str(exc)}), 422

    @app.errorhandler(ValidationError)
    def manejar_validacion(exc: ValidationError):
        return jsonify({"detalle": "Datos inválidos", "errores": exc.errors()}), 400

    app.register_blueprint(alumnos.bp, url_prefix=settings.API_V1_PREFIX)
    app.register_blueprint(asistencia.bp, url_prefix=settings.API_V1_PREFIX)
    app.register_blueprint(acciones.bp, url_prefix=settings.API_V1_PREFIX)
    app.register_blueprint(reportes.bp, url_prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
