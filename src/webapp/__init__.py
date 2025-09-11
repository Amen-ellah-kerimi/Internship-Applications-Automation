from flask import Flask
# TODO: NOTE: You can load config from config.yaml here if needed
# TODO: FIXME: Ensure thread-safe behavior when using internship_scraper in routes

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The Flask app instance.

    Notes:
        - All blueprints/routes should be registered here.
        - Config can be loaded from a YAML file or environment variables.
        - This function makes the app testable and avoids global state.
    """
    app = Flask(__name__)
    
    # TODO: Register blueprints (if you modularize routes)
    # from .routes import main_bp
    # app.register_blueprint(main_bp)

    return app

