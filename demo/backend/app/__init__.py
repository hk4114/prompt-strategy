from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Database configuration
    db_type = os.getenv('DB_TYPE', 'sqlite')

    if db_type == 'mysql':
        # MySQL configuration
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '3306')
        DB_USER = os.getenv('DB_USER', 'root')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        DB_NAME = os.getenv('DB_NAME', 'prompt_strategy')

        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        )
    else:
        # SQLite configuration (default for development)
        sqlite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'prompt_strategy.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{sqlite_path}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    from .routes.categories import categories_bp
    from .routes.prompts import prompts_bp
    from .routes.templates import templates_bp
    from .routes.tips import tips_bp

    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(prompts_bp, url_prefix='/api/prompts')
    app.register_blueprint(templates_bp, url_prefix='/api/templates')
    app.register_blueprint(tips_bp, url_prefix='/api/tips')

    # Create tables
    with app.app_context():
        db.create_all()

    return app
