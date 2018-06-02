"""
功能：登录验证装饰器
author：simon
"""

from django.shortcuts import redirect

from user.models import Users


def is_login(func):
    """
    登录验证装饰器
    :param func:
    :return:
    """
    def check_login(request):
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return redirect('user:login')

        user = Users.objects.filter(ticket=ticket).first()
        if not user:
            return redirect('user:login')
        request.user = user
        return func(request)
    return check_login
