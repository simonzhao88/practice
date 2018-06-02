import random

from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Users, Role

"""django自带的登录注册"""


def djregister(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'register.html')

    username = request.POST.get('username')
    pwd1 = request.POST.get('pwd1')
    pwd2 = request.POST.get('pwd2')

    if not all([username, pwd1, pwd2]):
        msg = '请填写完所有参数'
        return render(request, 'register.html', {'msg': msg})

    if pwd1 != pwd2:
        msg = '两次密码不一致'
        return render(request, 'register.html', {'msg': msg})
    User.objects.create_user(username=username, password=pwd1)
    return redirect('user:djlogin')


def djlogin(request):
    """
    登录验证
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username')
    pwd = request.POST.get('password')
    # 返回验证成功的信息，验证失败则为空
    user = auth.authenticate(username=username, password=pwd)

    if user:
        # 注册
        auth.login(request, user)
        return redirect('stu:index')
    else:
        msg = '用户名或密码错误'
        return render(request, 'login.html', {'msg': msg})


def djlogout(request):
    """
    登出操作
    :param request:
    :return:
    """
    if request.method == 'GET':
        auth.logout(request)
        return render(request, 'login.html')


"""自己用代码实现登录注册"""


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    username = request.POST.get('username')
    pwd1 = request.POST.get('pwd1')
    pwd2 = request.POST.get('pwd2')

    if not all([username, pwd1, pwd2]):
        msg = '注册信息不能为空'
        return render(request, 'register.html', {'msg': msg})
    if pwd1 != pwd2:
        msg = '两次密码必须一致'
        return render(request, 'register.html', {'msg': msg})
    password = make_password(password=pwd1)

    Users.objects.create(username=username, password=password)
    return redirect('user:login')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username')
    pwd = request.POST.get('password')

    user = Users.objects.filter(username=username).first()
    if user and check_password(pwd, user.password):
        # 先产生随机的字符串，长度28
        s = 'abcdefghijklmnopqrstuvwxyz1234567890'
        ticket = ''
        for i in range(28):
            ticket += random.choice(s)

        # 保存在服务端
        user.ticket = ticket
        user.save()

        # 保存在客户端
        response = redirect('stu:index')
        response.set_cookie('ticket', ticket)

        return response
    else:
        msg = '用户名或密码错误'
        return render(request, 'login.html', {'msg': msg})


def logout(request):
    if request.method == 'GET':
        response = redirect('user:login')
        response.delete_cookie('ticket')
        # user = Users.objects.filter(username=request.user).first()
        # user.ticket = ''
        # user.save()
        return response


def userper(request):
    if request.method == 'GET':
        # 查询妲己拥有哪些权限
        u_r_p = Users.objects.filter(username='小妲己').first().role.r_p.all()

        # 判断妲己是否有学生列表权限
        u_r_p.filter(p_en='STUDENTLIS').exist()
    return '123'
