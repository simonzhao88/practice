from django.contrib import admin

# Register your models here.
from cart.models import Goods


class GoodsAdmin(admin.ModelAdmin):
    """
    确定要显示的列以及根据名字查询
    """
    list_display = ('id', 'name', 'price', 'image')
    search_fields = ('name',)


admin.site.register(Goods, GoodsAdmin)
