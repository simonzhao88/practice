import os
import re
import time

from flask import render_template, session, request, jsonify
from flask_restful import Resource

from App.main import main
from App.models import User, db
from config import Config
from exts_init import api
from utils import status_code
from utils.login_required import login_required


@main.route('/index/')
def index():
    return render_template('index.html')


@main.route('/mine/')
@login_required
def mine():
    return render_template('my.html')


@main.route('/profile/')
@login_required
def profile():
    return render_template('profile.html')


class MineApi(Resource):
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
    def patch(self):
        file = request.files.get('avatar')
        name = request.form.get('name')
        user = User.query.get(session['u_id'])
        if file:
            if not re.match(r'image/.*', file.mimetype):
                return jsonify(status_code.USER_CHANGE_PROFILE_IMAGES_ERROR)

            # 保存
            filename = str(int(time.time() * 100)) + file.filename
            image_path = os.path.join(Config.UPLOAD_DIR, filename)
            file.save(image_path)

            avatar_path = os.path.join('upload', filename)
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


api.add_resource(MineApi, '/api/mine/')
api.add_resource(ProfileApi, '/api/profile/')
