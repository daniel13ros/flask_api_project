from flask import Flask, jsonify
from .DB.database import Database
from .utils.errors import AppError

from .routes.task_route import task_bp
from .routes.user_route import user_bp
from .routes.category_route import category_bp

def create_app():
    app = Flask(__name__)
    
    Database.initialize()

    app.register_blueprint(task_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(user_bp)

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({
            "status": "error",
            "message": error.message,
            "details": error.payload
        }), error.status_code
    return app