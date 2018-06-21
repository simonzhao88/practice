from datetime import datetime

from flask import render_template, request, jsonify, session
from flask_restful import Resource

from App.models import Order
from App.order import order
from exts_init import api
from utils import status_code
from utils.login_required import login_required


@order.route('/myorder/')
def my_order():
    return render_template('orders.html')


class OrderApi(Resource):
    @login_required
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
        order.house_price = price
        order.amount = order.days * order.house_price

        try:
            order.add_update()
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)
        return jsonify(status_code.SUCCESS)


api.add_resource(OrderApi, '/api/order/')
