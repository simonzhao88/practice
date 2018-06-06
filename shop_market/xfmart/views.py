from django.shortcuts import render
from django.urls import reverse

from user.models import UserTicketModel
from utils.toolfuncs import get_order_random_id
from .models import MainWheel, MainNav, MainMustbuy, MainShop, \
    MainShow, Goods, FoodType, CartModel, OrderModel, OrderGoodsModel
from django.http import HttpResponseRedirect, JsonResponse


def index(request):
    """
    首页页面
    :param request:
    :return:
    """
    if request.method == 'GET':
        title = '首页'
        banners = MainWheel.objects.all()
        navs = MainNav.objects.all()
        mustbuys = MainMustbuy.objects.all()
        shops = MainShop.objects.all()
        shows = MainShow.objects.all()
        ctx = {
            'title': title, 'banners': banners, 'navs': navs,
            'mustbuys': mustbuys, 'shops1': shops[0], 'shops2': shops[1:3],
            'shops3': shops[3:7], 'shops4': shops[7:11], 'shows': shows
        }
        return render(request, 'home/home.html', context=ctx)


def market(request):
    """
    重定向到闪购页面
    :param request:
    :return:
    """
    return HttpResponseRedirect(reverse('xf:market_param',
                                        args=('104749', '0', '0')))


def user_market(request, typeid, cid, sid):
    """
    闪购页面
    :param request:
    :param typeid: 分类id
    :param cid: 子分类id
    :param sid: 排序id
    """
    if request.method == 'GET':
        foodtypes = FoodType.objects.all()
        # 根据子分类cid筛选数据
        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid, childcid=cid)
        # 根据排序排序cid进行数据排序
        if sid == '1':
            goods = goods.order_by('productnum')
        elif sid == '2':
            goods = goods.order_by('-price')
        elif sid == '3':
            goods = goods.order_by('price')
        # 将数据库里的分类名（全部分类:0#进口水果:103534#国产水果:103533）
        # 数据处理为[[全部分类，0],[进口水果，103534],[国产水果，103533]]
        foodtypes_current = FoodType.objects.filter(typeid=typeid).first().childtypenames
        if foodtypes_current:
            types = foodtypes_current.split('#')
            child_list = []
            for i in types:
                child_type_info = i.split(':')
                child_list.append(child_type_info)
        ctx = {
            'title': '闪购超市',
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'childs': child_list,
            'cid': cid
        }

        return render(request, 'market/market.html', context=ctx)


def cart(request):
    """
    购物车
    :param request:
    :return:
    """
    if request.method == 'GET':
        user = request.user
        if user.id:
            carts = CartModel.objects.filter(user=user)
            ctx = {
                'carts': carts
            }
        return render(request, 'cart/cart.html', context=ctx)


def mine(request):
    """
    个人中心
    :param request:
    :return:
    """
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        try:
            user = UserTicketModel.objects.filter(ticket=ticket).first().user
        except AttributeError:
            user = None
        return render(request, 'mine/mine.html', {'user': user, 'title': '个人中心'})


def add_cart(request):
    """
    添加商品到购物车
    :param request:
    :return:
    """
    if request.method == 'POST':
        user = request.user
        goods_id = request.POST.get('goods_id')
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        # 判断用户是否是系统自带的anonymouseuser还是登陆的用户
        if user.id:
            user_cart = CartModel.objects.filter(user_id=user.id,
                                                 goods_id=goods_id).first()

            if user_cart:
                user_cart.c_num += 1
                user_cart.save()
                data['c_num'] = user_cart.c_num
            else:
                CartModel.objects.create(user=user,
                                         goods_id=goods_id)
                data['c_num'] = 1
            return JsonResponse(data)
        data['msg'] = '您还未登陆，请去登陆~'
        data['code'] = 403

        return JsonResponse(data)


def sub_cart(request):
    """
    删除商品到购物车
    :param request:
    :return:
    """
    if request.method == 'POST':
        user = request.user
        goods_id = request.POST.get('goods_id')
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        # 判断用户是否是系统自带的anonymouseuser还是登陆的用户
        if user.id:
            user_cart = CartModel.objects.filter(user_id=user.id,
                                                 goods_id=goods_id).first()

            if user_cart:
                if user_cart.c_num == 1:
                    user_cart.delete()
                    data['c_num'] = 0
                else:
                    user_cart.c_num -= 1
                    user_cart.save()
                    data['c_num'] = user_cart.c_num
            else:
                data['code'] = 400
                data['msg'] = '购物车没有这件商品'
            return JsonResponse(data)
        data['msg'] = '您还未登陆，请去登陆~'
        data['code'] = 403

        return JsonResponse(data)


def goods_num(request):
    """
    显示闪购页面用户加入购物车商品的数量
    :param request:
    :return:
    """
    if request.method == 'POST':
        user = request.user
        goods_id = request.POST.get('goods_id')
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        # 判断用户是否是系统自带的anonymouseuser还是登陆的用户
        if user.id:
            user_cart = CartModel.objects.filter(user_id=user.id,
                                                 goods_id=goods_id).first()

            if user_cart:
                data['c_num'] = user_cart.c_num
        return JsonResponse(data)


def change_status(request):
    """
    修改购物车商品选择状态
    :param request:
    :return:
    """
    data = {
        'code': 200,
        'msg': '请求成功'
    }
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart = CartModel.objects.filter(id=cart_id).first()
        is_select = request.POST.get('isselect')
        if not is_select:
            if cart.is_select:
                cart.is_select = False
                data['check'] = cart.is_select
            else:
                cart.is_select = True
                data['check'] = cart.is_select
        elif is_select == '1':
            cart.is_select = True
        else:
            cart.is_select = False

        cart.save()
    return JsonResponse(data)


def generate_order(request):
    """
    下单
    :param request:
    :return:
    """
    if request.method == 'GET':
        user = request.user

        o_num = get_order_random_id()
        OrderModel.objects.create(user=user, o_num=o_num)
        order = OrderModel.objects.filter(o_num=o_num).first()
        user_carts = CartModel.objects.filter(user=user, is_select=True)
        for cart in user_carts:
            goods = cart.goods
            goods_num = cart.c_num
            OrderGoodsModel.objects.create(goods=goods, order=order, goods_num=goods_num)
            cart.delete()
        ctx = {
            'o_num': o_num,
            'carts': user_carts,
        }
    return render(request, 'order/order_info.html', context=ctx)
