from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.loginview = 'auth.login'


def create_app(development):
    app = Flask(__name__)
    app.config.from_object(config[development])
    config[development].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # 附加路由和自定义的错误页面
    login_manager.init_app(app)
    return app
