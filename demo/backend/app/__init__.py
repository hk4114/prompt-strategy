from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    CORS(app)
    db.init_app(app)
    
    # 注册蓝图
    from app.routes.categories import categories_bp
    from app.routes.templates import templates_bp
    from app.routes.prompts import prompts_bp
    from app.routes.tips import tips_bp
    
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(templates_bp, url_prefix='/api/templates')
    app.register_blueprint(prompts_bp, url_prefix='/api/prompts')
    app.register_blueprint(tips_bp, url_prefix='/api/tips')
    
    return app
