# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-31 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stu', '0003_student_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='s_sex',
            field=models.BooleanField(default=True),
        ),
    ]
