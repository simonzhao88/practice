from django.shortcuts import render
from django.urls import reverse

from user.models import UserTicketModel
from .models import MainWheel, MainNav, MainMustbuy, MainShop, \
    MainShow, Goods, FoodType
from django.http import HttpResponseRedirect


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
    return render(request, 'cart/cart.html')


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
