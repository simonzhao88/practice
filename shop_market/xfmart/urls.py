from django.conf.urls import url

from xfmart import views

urlpatterns = [
    # 首页
    url(r'^home/', views.index, name='home'),
    # 闪购页面
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.user_market, name='market_param'),
    # 购物车
    url(r'^cart/', views.cart, name='cart'),
    # 我的页面
    url(r'^mine/', views.mine, name='mine'),
]
