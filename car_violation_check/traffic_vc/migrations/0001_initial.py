# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-23 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trecord',
            fields=[
                ('no', models.CharField(db_column='r_no', max_length=12, primary_key=True, serialize=False, verbose_name='记录编号')),
                ('lic_plate', models.CharField(db_column='license_plate', max_length=12, verbose_name='车牌')),
                ('reason', models.CharField(max_length=100, verbose_name='违章原因')),
                ('v_date', models.DateTimeField(verbose_name='违章时间')),
                ('punishment', models.CharField(blank=True, max_length=100, null=True, verbose_name='处罚方式')),
                ('is_accept', models.BooleanField(default=0, verbose_name='是否受理')),
            ],
            options={
                'db_table': 'tb_record',
            },
        ),
    ]
