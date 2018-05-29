from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from user.models import Users


class UserAuthMiddle(MiddlewareMixin):
    """
    自己编写中间件，实现登录验证功能，有坑 就是每个页面都会验证导致登录页面会出现
    重定向次数多刷不出页面，需要通过一个判断 筛出登录和注册页面
    """

    def process_request(self, request):

        # 验证cookies中的ticket，验证不通过，跳转到登录
        # 验证通过，request.user当前登录的用户信息
        # return None 或者不写return

        path = request.path
        pdir = ['/user/login', '/user/register/']
        if path in pdir:
            return None

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return redirect('user:login')

        user = Users.objects.filter(ticket=ticket)
        if not user:
            return redirect('user:login')

        request.user = user
