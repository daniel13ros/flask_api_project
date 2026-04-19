from flask import Flask, jsonify, render_template
from utils.errors import AppError
from routes.user_route import user_bp
from routes.task_route import task_bp
from routes.category_route import category_bp
from routes.log_route import log_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app) 


    # Blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(task_bp, url_prefix='/api')
    app.register_blueprint(category_bp, url_prefix='/api')
    app.register_blueprint(log_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return render_template('index.html')

    # Global Error Handler
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({"error": error.message}), error.status_code

    return app

if __name__ == '__main__':
    create_app().run(debug=True)