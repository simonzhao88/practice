from flask import Flask
from config import config, Config
from exts_init import ext_init


def create_app(development):
    app = Flask(__name__,
                static_folder=Config.STATIC_DIR,
                template_folder=Config.TEMPLATES_DIR)
    app.config.from_object(config[development])
    config[development].init_app(app)
    from App.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from App.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    ext_init(app)
    return app
