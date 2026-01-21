from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # 配置
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'prompt_strategy.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_AS_ASCII'] = False

    # 初始化扩展
    db.init_app(app)
    CORS(app)

    # 注册蓝图
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # 创建数据库表
    with app.app_context():
        db.create_all()
        
        # 初始化默认数据
        from app.utils.init_data import init_default_templates, init_categories, init_tips
        init_default_templates(app)
        init_categories(app)
        init_tips(app)

    return app
