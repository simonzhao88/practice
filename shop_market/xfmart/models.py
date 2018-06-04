from django.db import models

from user.models import UserModel


class Main(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    trackid = models.CharField(max_length=16)

    class Meta:
        abstract = True


class MainWheel(Main):
    """首页banner"""
    class Meta:
        db_table = 'xf_wheel'


class MainNav(Main):
    """首页导航栏"""
    class Meta:
        db_table = 'xf_nav'


class MainMustbuy(Main):
    """必购"""
    class Meta:
        db_table = 'xf_mustbuy'


class MainShop(Main):
    """首页商店"""
    class Meta:
        db_table = 'xf_shop'


class MainShow(Main):
    """首页商品展示"""
    categoryid = models.CharField(max_length=16)
    brandname = models.CharField(max_length=100)   # 分类名称

    img1 = models.CharField(max_length=200)   # 图片
    childcid1 = models.CharField(max_length=16)   # 子类id
    productid1 = models.CharField(max_length=16)
    longname1 = models.CharField(max_length=100)   # 商品名称
    price1 = models.FloatField(default=0)   # 折后价
    marketprice1 = models.FloatField(default=1)   # 原价

    img2 = models.CharField(max_length=200)  # 图片
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)  # 商品名称
    price2 = models.FloatField(default=0)  # 折后价
    marketprice2 = models.FloatField(default=1)  # 原价

    img3 = models.CharField(max_length=200)  # 图片
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)  # 商品名称
    price3 = models.FloatField(default=0)  # 折后价
    marketprice3 = models.FloatField(default=1)  # 原价

    class Meta:
        db_table = 'xf_mainshow'


# 闪购页面-左侧类型表
class FoodType(models.Model):
    """商品类型表"""
    typeid = models.CharField(max_length=16)   # 分类id
    typename = models.CharField(max_length=100)   # 商品分类名称
    childtypenames = models.CharField(max_length=200)   # 商品
    typesort = models.IntegerField(default=1)   # 排序

    class Meta:
        db_table = 'xf_foodtypes'


class Goods(models.Model):
    """商品表"""
    productid = models.CharField(max_length=16)  # 商品id
    productimg = models.CharField(max_length=200)   # 商品图片
    productname = models.CharField(max_length=100)   # 商品名称
    productlongname = models.CharField(max_length=200)  # 商品长名称
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)   # 规格
    price = models.FloatField(default=0)   # 折后价
    marketprice = models.FloatField(default=1)   # 原价
    categoryid = models.CharField(max_length=16)  # 分类id
    childcid = models.CharField(max_length=16)   # 子分类id
    childcidname = models.CharField(max_length=100)  # 名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)  # 排序
    productnum = models.IntegerField(default=1)   # 销量排序

    class Meta:
        db_table = 'xf_goods'


class CartModel(models.Model):
    """购物车表"""
    user = models.ForeignKey(UserModel)  # 关联用户
    goods = models.ForeignKey(Goods)   # 关联商品
    c_num = models.IntegerField(default=1)    # 商品数量
    is_select = models.BooleanField(default=True)   # 是否选中

    class Meta:
        db_table = 'xf_cart'


class OrderModel(models.Model):
    """订单表"""
    user = models.ForeignKey(UserModel)   # 关联用户
    o_num = models.CharField(max_length=64)  # 订单数量
    # 0 表示已下单，但未付款， 1 已付款未发货， 2 已付款已发货
    o_status = models.IntegerField(default=0)   # 状态
    o_create = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        db_table = 'xf_order'


class OrderGoodsModel(models.Model):
    """商品订单关联表"""
    goods = models.ForeignKey(Goods)   # 关联商品
    order = models.ForeignKey(OrderModel)   # 关联的订单
    goods_num = models.IntegerField(default=1)   # 商品数量

    class Meta:
        db_table = 'xf_order_goods'

