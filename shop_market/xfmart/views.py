from django.shortcuts import render, redirect

from user.models import UserTicketModel
from .models import MainWheel, MainNav, MainMustbuy, MainShop, MainShow, UserModel
from django.http import HttpResponse


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
    pass


def cart(request):
    pass


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
        return render(request, 'mine/mine.html', {'user': user})

