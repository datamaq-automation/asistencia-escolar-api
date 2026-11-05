from flask import Flask

from src.main import create_app


def test_create_app_returns_flask_app() -> None:
    app = create_app()

    assert isinstance(app, Flask)
    assert any(rule.startswith("/api/v1/alumnos") for rule in [r.rule for r in app.url_map.iter_rules()])
