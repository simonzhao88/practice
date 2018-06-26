import os
import re

from flask import render_template, jsonify, request, session
from flask_restful import Resource

from App.house import house
from App.models import Area, Facility, House, db, HouseImage, User, Order
from config import Config
from exts_init import api
from utils import status_code

#
# @house.route('/index/')
# def index():
#     return render_template('index.html')
from utils.login_required import login_required


@house.route('/index/')
@house.route('/')
def index():
    return render_template('index.html')


@house.route('/myhouse/')
@login_required
def my_house():
    return render_template('myhouse.html')


@house.route('/newhouse/')
@login_required
def new_house():
    return render_template('newhouse.html')


@house.route('/area_facility/')
def area_facility():
    """
    获取房屋设施及地区接口
    :return:
    """
    areas = Area.query.all()
    facilitys = Facility.query.all()

    areas_list = [area.to_dict() for area in areas]
    facilitys_list = [facility.to_dict() for facility in facilitys]
    return jsonify(code=200, areas=areas_list, facilitys=facilitys_list)


@house.route('/detail/')
def detail():
    return render_template('detail.html')


@house.route('/booking/')
def booking():
    return render_template('booking.html')


@house.route('/search/')
def search():
    return render_template('search.html')


class HouseApi(Resource):
    @login_required
    def get(self):
        """
        获取房屋信息接口
        :return:
        """
        user_id = session['u_id']
        houses = House.query.filter_by(user_id=user_id)
        u = User.query.get(user_id)
        if not u.id_name:
            return jsonify(status_code.USER_AUTH_NOT_AUTHENTICATION)
        return jsonify({
            'code': status_code.OK,
            'data': [house.to_dict() for house in houses]
        })

    @login_required
    def post(self):
        """
        添加房源接口
        :return:
        """
        user_id = session['u_id']
        title = request.form.get('title')
        price = request.form.get('price')
        area_id = request.form.get('area_id')
        address = request.form.get('address')
        room_count = request.form.get('room_count')
        acreage = request.form.get('acreage')
        unit = request.form.get('unit')
        capacity = request.form.get('capacity')
        beds = request.form.get('beds')
        deposit = request.form.get('deposit')
        min_days = request.form.get('min_days')
        max_days = request.form.get('max_days')
        facilitys = request.form.get('facilitys')
        if not all([title, price, area_id, address, room_count, acreage, unit,
                    capacity, beds, deposit, min_days, max_days, facilitys]):
            return jsonify(status_code.HOUSE_ADD_DATA_IS_NOT_NULL)

        house = House(user_id=user_id, title=title, price=price, area_id=area_id,
                      address=address, room_count=room_count, acreage=acreage, unit=unit,
                      capacity=capacity, beds=beds, deposit=deposit, min_days=min_days,
                      max_days=max_days)
        facility_list = facilitys.split(',')
        for facility in facility_list:
            facility = Facility.query.get(facility)
            house.facilities.append(facility)
        try:
            house.add_update()
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)
        house_id = house.id
        return jsonify({
            'code': 200,
            'msg': '请求成功~',
            'house_id': house_id
        })


class HouseImageAPI(Resource):
    @login_required
    def post(self):
        """
        添加房屋图片接口
        :return:
        """
        images = request.files.getlist('house_image')
        house_id = request.form.get('house_id')
        path = os.path.join(Config.UPLOAD_HOUSE_IMAGE_DIR, house_id)

        # 保存房屋首图
        house = House.query.get(house_id)
        if not os.path.exists(path):
            os.makedirs(path)
        for file in images:
            if not re.match(r'image/.*', file.mimetype):
                return jsonify(status_code.USER_CHANGE_PROFILE_IMAGES_ERROR)
            filepath = str(house_id) + '\\' + file.filename
            image_path = os.path.join(Config.UPLOAD_HOUSE_IMAGE_DIR, filepath)
            file.save(image_path)
            house_image = HouseImage()
            house_image.house_id = house_id
            house_image.url = os.path.join('upload', filepath)
            if not house.index_image_url:
                house.index_image_url = os.path.join('upload', filepath)
            try:
                house_image.add_update()
                house.add_update()
            except Exception as e:
                db.session.rollback()
                return jsonify(status_code.DATABASE_ERROR)
        return jsonify(status_code.SUCCESS)


class HouseDetailApi(Resource):
    def get(self):
        """
        获取房屋详情数据接口
        :return:
        """
        user_id = session.get('u_id')
        house_id = request.args.get('house_id')
        house_detail = House.query.get(house_id)
        if house_detail:
            return jsonify({
                'code': 200,
                'data': house_detail.to_full_dict(),
                'u_id': user_id
            })
        else:
            return jsonify(status_code.HOUSE_QUERY_ERROR)


class IndexApi(Resource):
    def get(self):
        """
        获取首页页面数据接口
        :return:
        """
        username = ''
        user_id = session.get('u_id')
        if user_id:
            username = User.query.get(user_id).name

        houses = House.query.order_by(House.id.desc()).all()
        return jsonify(code=200, username=username,
                       houses=[house.to_dict() for house in houses])


class SearchApi(Resource):
    def get(self):
        aid = request.args.get('aid')  # 区域id
        sd = request.args.get('sd')  # 入住时间
        ed = request.args.get('ed')  # 离开时间
        sk = request.args.get('sk')  # 排序规则

        # 通过区域搜索房屋
        house = House.query.filter(House.area_id == aid)

        # 过滤自己的房屋信息
        if 'u_id' in session:
            house = house.filter(House.user_id != session['u_id'])

        # 判断搜索的入住时间和离开时间的订单
        order = Order.query.filter(Order.status == "PAID")
        order1 = order.filter(Order.begin_date >= sd, Order.end_date <= ed).all()
        order2 = order.filter(Order.begin_date >= sd, Order.begin_date <= ed).all()
        order3 = order.filter(Order.end_date >= sd, Order.end_date <= ed).all()
        order4 = order.filter(Order.begin_date <= sd, Order.end_date >= ed).all()

        # 去重
        order_list = list(set(order1 + order2 + order3 + order4))

        house_ids = [order.to_dict().house_id for order in order_list]
        # 将已被预约的房屋筛选出去并按要求排序
        if sk == 'booking':
            houses = house.filter(House.id.notin_(house_ids)).order_by(House.order_count)
        elif sk == 'price-inc':
            houses = house.filter(House.id.notin_(house_ids)).order_by(House.price)
        elif sk == 'new':
            houses = house.filter(House.id.notin_(house_ids)).order_by(House.create_time.desc())
        else:
            houses = house.filter(House.id.notin_(house_ids)).order_by(House.price.desc())
        house_info = [house.to_dict() for house in houses]

        return jsonify(code=status_code.OK, house_info=house_info)


api.add_resource(HouseApi, '/api/house/')
api.add_resource(HouseImageAPI, '/api/house/image/')
api.add_resource(HouseDetailApi, '/api/house/detail/')
api.add_resource(IndexApi, '/api/house/index/')
api.add_resource(SearchApi, '/api/house/search/')
