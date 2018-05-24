from django.contrib import admin

from traffic_vc.models import Trecord


class TrecordAdmin(admin.ModelAdmin):
    list_display = ('lic_plate', 'reason', 'v_date', 'punishment', 'is_accept')


admin.site.register(Trecord, TrecordAdmin)
