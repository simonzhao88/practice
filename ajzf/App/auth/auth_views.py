import os
import re

from flask import render_template, request, jsonify, session, redirect, url_for
from flask_restful import Resource

from App.auth import auth
from App.models import User, db
from exts_init import api
from utils import status_code
from utils.login_required import login_required


@auth.route('/register/')
def register():
    return render_template('register.html')


@auth.route('/login/')
def login():
    return render_template('login.html')


@auth.route('/logout/')
@login_required
def logout():
    session.pop('u_id', None)
    return redirect(url_for('.login'))


class RegisterApi(Resource):
    def post(self):
        phone = request.form.get('mobile')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 验证数据完整性
        if not all([phone, password, password2]):
            return jsonify(status_code.USER_REGISTER_NOT_NULL)
        # 验证手机号码正确性
        if not re.match(r'^1[3456789]\d{9}$', phone):
            return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)
        if password != password2:
            return jsonify(status_code.USER_REGISTER_PASSWORD_IS_NOT_VALID)
        u = User.query.filter_by(phone=phone).all()
        # 如果已经存在此用户，则返回错误信息
        if u:
            return jsonify(status_code.USER_REGISTER_EXITS_USER)
        user = User()
        user.phone = phone
        user.password = password
        user.set_name(phone)
        db.session.add(user)
        db.session.commit()
        return {
            'code': 200,
            'msg': '注册成功~'
        }


class LoginApi(Resource):

    def post(self):
        phone = request.form.get('mobile')
        password = request.form.get('password')
        if not all([phone, password]):
            return jsonify(status_code.USER_LOGIN_NOT_NULL)
        u = User.query.filter_by(phone=phone).first()
        if u:
            # 验证密码是否正确
            if not u.verify_password(password):
                return jsonify(status_code.USER_LOGIN_PASSWORD_ERROE)
            session['u_id'] = u.id
            return {
                'code': status_code.OK,
                'msg': '登录成功~'
            }
        else:
            # 没有此用户则返回错误信息
            return jsonify(status_code.USER_LOGIN_MOBILE_ERROE)


api.add_resource(RegisterApi, '/auth/register/')
api.add_resource(LoginApi, '/auth/login/')
