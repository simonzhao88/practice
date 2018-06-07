import random
import time

from xfmart.models import CartModel


def get_ticket():
    """
    生成随机ticket
    :return:
    """
    s = 'abcdefghijklmnopqrstuvwxyz1234567890_*='
    ticket = ''
    for i in range(28):
        ticket += random.choice(s)
    return 'TK_' + ticket


def get_order_random_id():
    """
    生成时间戳构建的订单编号
    :return:
    """
    order = int(time.time()*1000)
    return order


def get_total_price(user):
    """
    计算购物车商品总价
    :param user:
    :return:
    """
    carts = CartModel.objects.filter(user=user, is_select=True)
    total_price = 0
    for cart in carts:
        price = cart.goods.price
        c_num = cart.c_num
        total_price += price * c_num
    return total_price
