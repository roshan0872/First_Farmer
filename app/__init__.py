import os
from flask import Flask, render_template, session, request, g, jsonify
from dotenv import load_dotenv

# Load local environment variables from .env
load_dotenv()

from app.config import configs
from app.extensions import db, migrate, csrf
from app.services.security import get_current_user
from app.services.i18n import load_translations, get_current_language, t, get_entity_translation
from app.cli import register_cli_commands

def create_app(config_name: str | None = None) -> Flask:
    """Application factory for First Farmer Agriculture System."""
    if not config_name:
        config_name = os.environ.get("APP_ENV", "development").lower()

    app = Flask(__name__, instance_relative_config=True)
    config_class = configs.get(config_name, configs["development"])
    app.config.from_object(config_class())

    # Ensure instance folder exists for local SQLite database
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Exempt specific API routes from CSRF if using token or JSON headers where applicable,
    # or keep CSRF on all state changing requests as specified in prompt.
    # We will exempt /api/chat if guest calls, but Flask-WTF protects forms.

    # Load i18n JSON files
    load_translations(app.root_path)

    # Register CLI commands
    register_cli_commands(app)

    # Context Processors & Template Globals
    @app.before_request
    def load_user_into_g():
        g.current_user = get_current_user()
        g.current_lang = get_current_language()

    @app.context_processor
    def inject_helpers():
        return {
            "t": t,
            "current_lang": get_current_language(),
            "current_user": g.current_user,
            "get_entity_translation": get_entity_translation,
        }

    # Security Headers
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Content Security Policy allowing local assets and vendored Chart.js
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self';"
        )
        response.headers["Content-Security-Policy"] = csp
        return response

    # Register Blueprints
    from app.blueprints.main.routes import main_bp
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.crops.routes import crops_bp
    from app.blueprints.guides.routes import guides_bp
    from app.blueprints.recommendations.routes import recommendations_bp
    from app.blueprints.weather.routes import weather_bp
    from app.blueprints.chatbot.routes import chatbot_bp
    from app.blueprints.learning.routes import learning_bp
    from app.blueprints.profile.routes import profile_bp
    from app.blueprints.admin.routes import admin_bp
    from app.blueprints.api.routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(crops_bp)
    app.register_blueprint(guides_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Bad request", "details": str(error)}), 400
        return render_template("errors/400.html"), 400

    @app.errorhandler(403)
    def forbidden(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Forbidden: Access denied"}), 403
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Resource not found"}), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Internal server error"}), 500
        return render_template("errors/500.html"), 500

    return app

