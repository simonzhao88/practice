from datetime import datetime

from flask import render_template, request, jsonify, session
from flask_restful import Resource

from App.models import Order, House, User
from App.order import order
from exts_init import api
from utils import status_code
from utils.login_required import login_required, check_login


@order.route('/myorder/')
def my_order():
    return render_template('orders.html')


@order.route('/customer_order/')
def customer_order():
    return render_template('lorders.html')


class OrderApi(Resource):
    @check_login
    def post(self):
        user_id = session['u_id']
        house_id = request.form.get('house_id')
        price = request.form.get('price')
        begin_date = datetime.strptime(request.form.get('begin_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        if not all([house_id, begin_date, end_date]):
            return jsonify(status_code.DATA_NOT_FULL)
        if begin_date > end_date:
            return jsonify(status_code.CREATE_ORDER_END_DATA_ERROR)
        order = Order()
        order.user_id = user_id
        order.house_id = house_id
        order.begin_date = begin_date
        order.end_date = end_date
        order.days = (end_date - begin_date).days + 1
        order.house_price = int(price)
        order.amount = order.days * order.house_price

        try:
            order.add_update()
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)
        return jsonify(status_code.SUCCESS)


class MyOrderApi(Resource):
    @login_required
    def get(self):
        user_id = session['u_id']
        orders = Order.query.filter_by(user_id=user_id)
        return jsonify(code=status_code.OK,
                       orders=[order.to_dict() for order in orders])


class CustomerOrderApi(Resource):
    @login_required
    def get(self):
        user_id = session['u_id']
        houses = House.query.filter_by(user_id=user_id)
        house_ids = [house.id for house in houses]
        orders = Order.query.filter(Order.house_id.in_(house_ids)).order_by(Order.id)
        return jsonify(code=status_code.OK,
                       orders=[order.to_dict() for order in orders])


class AcceptOrderApi(Resource):
    @login_required
    def patch(self):
        order_id = request.form.get('order_id')
        status = request.form.get('status')
        order = Order.query.get(order_id)
        if status == 'WAIT_PAYMENT':
            msg = '接单成功~'
        elif status == 'REJECTED':
            reject_reason = request.form.get('reject_reason')
            msg = '拒单成功~'
            order.comment = reject_reason
        order.status = status
        try:
            order.add_update()
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)
        return jsonify(code=200, msg=msg)


api.add_resource(OrderApi, '/api/order/')
api.add_resource(MyOrderApi, '/api/my/order/')
api.add_resource(CustomerOrderApi, '/api/customer/order/')
api.add_resource(AcceptOrderApi, '/api/accept/order/')
