# Generated by Django 2.0.5 on 2018-05-22 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrs', '0002_emp_mgr'),
    ]

    operations = [
        migrations.AddField(
            model_name='dept',
            name='excellent',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='emp',
            name='comm',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='emp',
            name='mgr',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
