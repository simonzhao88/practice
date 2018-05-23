from django.db import models

# Create your models here.


class Trecord(models.Model):
    no = models.CharField(max_length=12, primary_key=True, db_column='r_no', verbose_name='记录编号')
    lic_plate = models.CharField(max_length=12, db_column='license_plate', verbose_name='车牌')
    reason = models.CharField(max_length=100, verbose_name='违章原因')
    v_date = models.DateTimeField(verbose_name='违章时间')
    punishment = models.CharField(max_length=100, null=True, blank=True, verbose_name='处罚方式')
    is_accept = models.BooleanField(default=0, verbose_name='是否受理')

    class Meta:
        db_table = 'tb_record'
