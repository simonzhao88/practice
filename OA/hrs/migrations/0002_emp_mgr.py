# Generated by Django 2.0.5 on 2018-05-22 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp',
            name='mgr',
            field=models.IntegerField(null=True),
        ),
    ]