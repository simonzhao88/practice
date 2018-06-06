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

    # 添加购物车商品
    url(r'^addCart/', views.add_cart, name='addCart'),
    # 删除购物车商品
    url(r'^subCart/', views.sub_cart, name='subCart'),
    url(r'^goodsNum/', views.goods_num, name='goodsNum'),
    # 改变购物车商品状态
    url(r'^changeCartStatus/', views.change_status, name='changeCartStatus'),
    url(r'^generateOrder/', views.generate_order, name='generateOrder')
]
