import logging

from flask import Flask, jsonify, render_template
from pydantic import ValidationError

from src.domain.asistencia_escolar.exceptions import DatosInvalidosError
from src.infrastructure.flask.routers import acciones, alumnos, asistencia, reportes
from src.infrastructure.settings.config import get_settings
from src.infrastructure.settings.logger import logger
from src.infrastructure.sqlalchemy.database import engine
from src.infrastructure.sqlalchemy.models import orm_models


def create_app() -> Flask:
    settings = get_settings()
    logger.info("Inicializando la app '%s' en entorno '%s'", settings.PROJECT_NAME, settings.ENVIRONMENT)

    try:
        orm_models.Base.metadata.create_all(engine)

        app = Flask(
            __name__,
            template_folder="../templates",
            static_folder="../static",
        )
        app.config["JSON_SORT_KEYS"] = False
        app.config["JSON_AS_ASCII"] = False
        app.config["DEBUG"] = settings.DEBUG
        app.config["PROPAGATE_EXCEPTIONS"] = settings.DEBUG

        @app.route("/")
        def index():
            logger.debug("Acceso a la ruta raíz")
            return render_template("index.html")

        @app.errorhandler(DatosInvalidosError)
        def manejar_datos_invalidos(exc: DatosInvalidosError):
            logger.warning("Datos inválidos: %s", str(exc))
            return jsonify({"detalle": str(exc)}), 400

        @app.errorhandler(ValueError)
        def manejar_valor_invalido(exc: ValueError):
            logger.warning("Valor inválido: %s", str(exc))
            return jsonify({"detalle": str(exc)}), 422

        @app.errorhandler(ValidationError)
        def manejar_validacion(exc: ValidationError):
            logger.warning("Validación fallida: %s", exc.errors())
            return jsonify({"detalle": "Datos inválidos", "errores": exc.errors()}), 400

        @app.errorhandler(Exception)
        def manejar_error_interno(exc: Exception):
            logger.exception("Error no controlado en la API: %s", exc)
            return jsonify({"detalle": "Error interno del servidor"}), 500

        app.register_blueprint(alumnos.bp, url_prefix=settings.API_V1_PREFIX)
        app.register_blueprint(asistencia.bp, url_prefix=settings.API_V1_PREFIX)
        app.register_blueprint(acciones.bp, url_prefix=settings.API_V1_PREFIX)
        app.register_blueprint(reportes.bp, url_prefix=settings.API_V1_PREFIX)

        logger.info("App creada correctamente con prefijo %s", settings.API_V1_PREFIX)
        return app
    except Exception:
        logger.exception("Fallo al inicializar la aplicación Flask")
        raise


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.debug)
