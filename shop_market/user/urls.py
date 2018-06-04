from django.conf.urls import url

from user import views


urlpatterns = [
    # 注册
    url(r'^register/', views.register, name='register'),
    # 检查用户名是否存在
    url(r'^checkuser', views.check_user, name='checkuser'),
    # 登录
    url(r'^login/', views.login, name='login'),
    # 登出
    url(r'^logout/', views.logout, name='logout'),
]
