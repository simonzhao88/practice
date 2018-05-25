from django.shortcuts import render, redirect

# Create your views here.
from cart.models import Goods


def index(request):
    good_liist = Goods.objects.all()
    return render(request, 'goods.html', {'goods_list': good_liist})


class CartItem(object):

    def __init__(self, no, goods, amount=1):
        """
        购物车商品
        :param no: 商品id
        :param goods: 商品
        :param amount: 数量
        :return:
        """
        self.no = no
        self.goods = goods
        self.amount = amount

    @property
    def total(self):
        return self.goods.price * self.amount


class ShoppingCart(object):
    """
    购物车类
    """
    def __init__(self):
        self.num = 1
        self.items = {}

    def add_item(self, item):
        """
        添加商品到购物车
        :return:
        :item: 商品
        """
        if item.goods.id in self.items:
            self.items[item.goods.id].amount += item.amount
        else:
            self.items[item.goods.id] = item


    def d_amount(self, id):
        if id in self.items:
            if self.items[id].amount == 1:
                del self.items[id]
            else:
                self.items[id].amount -= 1


    def a_amount(self, id):
        if id in self.items:
            self.items[id].amount += 1


    def remove_item(self, id):
        """
        移除商品
        :return:
        """
        if id in self.items:
            self.items.pop(id)

    def clear_item(self):
        """
        清空购物车
        :return:
        """
        self.num = 0
        self.items.clear()

    @property
    def total(self):
        """
        总计价格
        :return:
        """
        val = 0
        for item in self.items.values():
            val += item.total
        return val



def add_to_cart(request, id):
    goods = Goods.objects.get(pk=id)
    cart = request.session.get('cart', ShoppingCart())
    cart.add_item(CartItem(cart.num, goods))
    cart.num += 1
    request.session['cart'] = cart
    return redirect('/')


def show_cart(request):
    cart = request.session.get('cart', None)
    cart_items = cart.items.values() if cart else []
    total = cart.total if cart else 0
    return render(request, 'cart.html', {'cart_items': cart_items, 'total':total})


def dev_amount(request, id):
    cart = request.session.get('cart', None)
    cart.d_amount(id)
    request.session['cart'] = cart
    return redirect('/show_cart')


def add_amount(request, id):
    cart = request.session.get('cart', None)
    cart.a_amount(id)
    request.session['cart'] = cart
    return redirect('/show_cart')


def del_good(request, id):
    cart = request.session.get('cart', None)
    cart.remove_item(id)
    request.session['cart'] = cart
    return redirect('/show_cart')


def clear_cart(request):
    cart = request.session.get('cart', None)
    cart.clear_item()
    request.session['cart'] = cart
    return redirect('/show_cart')