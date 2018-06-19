import random
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config

db = SQLAlchemy()


class BaseModel(object):
    # 定义基础的模型
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now,
                            onupdate=datetime.now)

    def add_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(BaseModel, db.Model):
    __tablename__ = 'ihome_user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    phone = db.Column(db.String(11), unique=True)
    password_hash = db.Column(db.String(228))
    name = db.Column(db.String(30), unique=True)
    avatar = db.Column(db.String(228))   # 头像
    id_name = db.Column(db.String(30))   # 实名认证姓名
    id_card = db.Column(db.String(18), unique=True)   # 身份证号

    # houses = db.relationship('House', backref='user')
    # orders = db.relationship('Order', backref='user')

    @property
    def password(self):
        return '密码不可读~'

    @password.setter
    # 加密密码
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码
    def verify_password(self, password):
        return check_password_hash(self.password_hash,
                                   password)

    def set_name(self, phone):
        random_list = random.sample(Config.CHARACTER, 2)
        self.name = phone + '_' + random_list[0] + random_list[1]

    def to_auth_dict(self):
        """
        序列化用户身份证信息
        :return:
        """
        return {
            'id_name': self.id_name,
            'id_card': self.id_card
        }

    def to_basic_dict(self):
        """
        序列化用户基础数据
        :return:
        """
        return {
            'id': self.id,
            'avatar': self.avatar,
            'name': self.name,
            'phone': self.phone
        }
