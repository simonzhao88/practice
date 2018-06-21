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
    from App.house import house as house_blueprint
    app.register_blueprint(house_blueprint, url_prefix='/house')
    from App.order import order as order_blueprint
    app.register_blueprint(order_blueprint, url_prefix='/order')
    ext_init(app)
    return app
