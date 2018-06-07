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
    # 改变购物车商品状态
    url(r'^changeCartStatus/', views.change_cart_status, name='changeCartStatus'),
    # 下单
    url(r'^generateOrder/', views.generate_order, name='generateOrder'),
    # 修改订单状态（支付）
    url(r'^changeOrderStatus/', views.change_order_status, name='changeOrderStatus'),
    # 待支付页面
    url(r'^waitPay/', views.wait_pay, name='waitPay'),
    # 待收货页面
    url(r'^orderPayed/', views.order_payed, name='orderPayed'),
    # 待支付跳转到支付页面
    url(r'^waitPaytoPay', views.wait_pay_to_pay, name='waitPaytoPay')
]
