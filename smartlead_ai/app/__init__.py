"""Flask uygulamasını oluşturan fabrika."""

from flask import Flask, jsonify
from flask_cors import CORS

from config import configurations
from .database import init_db
from .routes import api_bp, pages_bp


def create_app(environment="development"):
    app = Flask(__name__)

    app.config.from_object(
        configurations.get(
            environment,
            configurations["production"]
        )
    )

    if environment == "production" and (
        app.config["SECRET_KEY"] == "development-only-change-me"
        or not app.config["ADMIN_API_KEY"]
    ):
        raise RuntimeError(
            "Production requires SECRET_KEY and ADMIN_API_KEY."
        )

    # Wix sitesinin tarayıcı üzerinden API'ye bağlanmasına izin verir.
    CORS(
        app,
        resources={
            r"/api/sohbet": {
                "origins": app.config["CORS_ORIGINS"]
            },
            r"/api/leads": {
                "origins": app.config["CORS_ORIGINS"]
            },
        },
        methods=["GET", "POST"],
        allow_headers=["Content-Type", "Authorization"],
    )

    with app.app_context():
        init_db(app)

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return jsonify(basari=True, durum="aktif")

    return app
