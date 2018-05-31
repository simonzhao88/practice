from django.db import models


class Grade(models.Model):
    g_name = models.CharField(max_length=20)
    delete = models.BooleanField(default=False)
    g_create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_grade'


class Student(models.Model):
    s_name = models.CharField(max_length=20, null=False, unique=True)
    s_create_time = models.DateTimeField(auto_now_add=True)
    s_operate_time = models.DateTimeField(auto_now=True)
    s_sex = models.BooleanField(default=True)
    s_img = models.ImageField(upload_to='upload', null=True)
    delete = models.BooleanField(default=False)
    g = models.ForeignKey(Grade)

    class Meta:
        db_table = 'tb_student'

