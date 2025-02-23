from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import logging
from logging.handlers import RotatingFileHandler
import firebase_admin
from firebase_admin import credentials
from config import get_config
from routes.user import user_bp
from routes.admin import admin_bp

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(get_config())
    
    # Enable CORS
    CORS(app)
    
    # Initialize Firebase Admin SDK
    # In production, use service account credentials from environment variables
    try:
        firebase_admin.initialize_app()
    except ValueError:
        # App already initialized
        pass

    # Setup logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/devops_bootcamp.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('DevOps Bootcamp startup')

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "DevOps Bootcamp API is running"
        })

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f'Page not found: {request.url}')
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error has occurred"
        }), 500

    @app.errorhandler(400)
    def bad_request_error(error):
        app.logger.error(f'Bad Request: {error}')
        return jsonify({
            "error": "Bad Request",
            "message": str(error)
        }), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        app.logger.error(f'Unauthorized access attempt: {request.url}')
        return jsonify({
            "error": "Unauthorized",
            "message": "Authentication is required to access this resource"
        }), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        app.logger.error(f'Forbidden access attempt: {request.url}')
        return jsonify({
            "error": "Forbidden",
            "message": "You don't have permission to access this resource"
        }), 403

    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
