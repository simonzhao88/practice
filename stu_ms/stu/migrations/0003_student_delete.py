# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-31 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stu', '0002_student_s_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='delete',
            field=models.BooleanField(default=False),
        ),
    ]
