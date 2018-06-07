from datetime import datetime

from django.db.models import Q
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from user.models import UserTicketModel


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
        need_login = ['/xf/mine/', '/xf/cart/', '/xf/addCart/', '/xf/subCart/',
                      '/xf/goodsNum/', '/xf/generateOrder/', '/xf/changeOrderStatus/',
                      '/xf/waitPay/', '/xf/orderPayed/', '/xf/changeCartStatus/']   # 需要登录的页面
        if path not in need_login:
            return None

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return redirect('user:login')
        user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
        if user_ticket:
            # 获取到有认证的相关信息
            # 1.验证当前认证信息是否过期，如果没过期， request.user赋值
            # 2.如果过期，跳转到登录，并删除认证信息
            if datetime.utcnow() > user_ticket.out_time.replace(tzinfo=None):
                # 过期
                UserTicketModel.objects.filter(user=user_ticket.user).delete()
                return redirect('user:login')
            else:
                # 没过期  request.user赋值
                request.user = user_ticket.user
                UserTicketModel.objects.filter(Q(user=user_ticket.user) & ~Q(ticket=ticket)).delete()
