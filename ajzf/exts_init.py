from App.models import db

from flask_restful import Api

from flask_session import Session

api = Api()
se = Session()


def ext_init(app):
    db.init_app(app)
    api.init_app(app)
    se.init_app(app)
