import os

import redis

BASE_DIR = os.path.dirname(__file__)


class Config:
    CSRF_ENABLED = True
    CHARACTER = 'abcdefghijklmnopqrstuvwxyz'
    SECRET_KEY = os.urandom(16)
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379')
    GRADE_PER_PAGE = 5
    STUDENT_PER_PAGE = 5
    # 静态文件路径
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    # 模板文件路径
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    # 上传文件路径
    UPLOAD_DIR = os.path.join(os.path.join(BASE_DIR, 'static'), 'upload')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/ajzf'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASE_DIR, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
