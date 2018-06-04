import datetime
import json
import random

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect

from user.models import UserTicketModel
from xfmart.models import UserModel


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = make_password(request.POST.get('password'))
        icon = request.FILES.get('icon')
        UserModel.objects.create(username=username, email=email, password=password, icon=icon)
        return redirect('user:login')


def check_user(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        u = UserModel.objects.filter(username=username).first()
        if u:
            return HttpResponse(json.dumps({'status': 900, 'desc': '该用户名已被注册~'}))
        else:
            return HttpResponse(json.dumps({'status': 200, 'desc': '恭喜！用户名可用~'}))


def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserModel.objects.filter(username=username).first()
        out_time = datetime.datetime.now() + datetime.timedelta(days=7)
        if user and check_password(password, user.password):
            s = 'abcdefghijklmnopqrstuvwxyz1234567890_*='
            ticket = ''
            for i in range(28):
                ticket += random.choice(s)
            UserTicketModel.objects.create(ticket=ticket, out_time=out_time, user_id=user.id)
            response = redirect('xf:mine')
            response.set_cookie('ticket', ticket)
            return response
        else:
            msg = '用户名或密码错误'
            return render(request, 'user/user_login.html', {'msg': msg})


def logout(request):
    """
    登出
    :param request:
    :return:
    """
    if request.method == 'GET':
        response = redirect('user:login')
        ticket = request.COOKIES['ticket']
        response.delete_cookie('ticket')
        UserTicketModel.objects.filter(ticket=ticket).delete()
        return response

