import os
import re
import time

from flask import render_template, request, jsonify, session, redirect, url_for
from flask_restful import Resource

from App.auth import auth
from App.models import User, db
from config import Config
from exts_init import api
from utils import status_code
from utils.login_required import login_required


@auth.route('/register/')
def register():
    return render_template('register.html')


@auth.route('/login/')
def login():
    return render_template('login.html')


# @auth.route('/logout/')
# @login_required
# def logout():
#     session.pop('u_id', None)
#     return redirect(url_for('.login'))


@auth.route('/mine/')
@login_required
def mine():
    return render_template('my.html')


@auth.route('/profile/')
@login_required
def profile():
    return render_template('profile.html')


@auth.route('/authentication/')
@login_required
def authentication():
    return render_template('auth.html')


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


class LogoutApi(Resource):
    def delete(self):
        session.pop('u_id', None)
        return {
            'code': 200,
            'msg': '请求成功'
        }


class MineApi(Resource):
    @login_required
    def get(self):
        u_id = session.get('u_id')
        u = User.query.get(u_id)
        return {
            'code': 200,
            'msg': '请求成功~',
            'data': {
                'phone': u.phone,
                'name': u.name,
                'avatar': u.avatar
            }
        }


class ProfileApi(Resource):
    @login_required
    def patch(self):
        file = request.files.get('avatar')
        name = request.form.get('name')
        user = User.query.get(session['u_id'])
        if file:
            if not re.match(r'image/.*', file.mimetype):
                return jsonify(status_code.USER_CHANGE_PROFILE_IMAGES_ERROR)

            # 保存
            filename = str(int(time.time() * 100)) + file.filename
            image_path = os.path.join(Config.UPLOAD_AVATAR_DIR, filename)
            file.save(image_path)

            avatar_path = os.path.join('upload/avatar', filename)
            user.avatar = avatar_path
            try:
                user.add_update()
            except Exception as e:
                db.session.rollback()
                return jsonify(status_code.DATABASE_ERROR)
            return jsonify(code=status_code.OK, image_url=avatar_path)
        if name:
            u = User.query.filter_by(name=name).first()
            if u:
                return jsonify(status_code.USER_CHANGE_PROFILE_NAME_ERROR)
            user.name = name
            try:
                user.add_update()
            except Exception as e:
                db.session.rollback()
                return jsonify(status_code.DATABASE_ERROR)
            return jsonify(code=status_code.OK, msg='修改用户名成功~')


class AuthenticationApi(Resource):
    def get(self):
        user_id = User.query.get(session['u_id'])
        return jsonify(code=200, data=user_id.to_auth_dict())

    @login_required
    def patch(self):
        real_name = request.form.get('real_name')
        id_card = request.form.get('id_card')
        if not all([real_name, id_card]):
            return jsonify(status_code.USER_AUTH_DATA_IS_NOT_NULL)

        if not re.match(r'^[1-9]\d{17}$', id_card):
            return jsonify(status_code.USER_AUTH_ID_CARD_IS_NOT_VALID)

        user = User.query.get(session['u_id'])
        if user.id_name:
            return jsonify(status_code.USER_AUTH_IS_EXITS_ERROR)
        user.id_name = real_name
        user.id_card = id_card
        try:
            user.add_update()
        except Exception as e:
            db.session.rollback()
            return jsonify(status_code.DATABASE_ERROR)
        return jsonify(status_code.SUCCESS)


api.add_resource(RegisterApi, '/auth/register/')
api.add_resource(LoginApi, '/auth/login/')
api.add_resource(LogoutApi, '/auth/logout/')
api.add_resource(MineApi, '/api/mine/')
api.add_resource(ProfileApi, '/api/profile/')
api.add_resource(AuthenticationApi, '/api/authentication/')

