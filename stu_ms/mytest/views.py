from django.db.models import Q, F
from django.shortcuts import render

from mytest.models import StuInfo, Student, Grade


def test(request):
    # 1.通过某个学生拓展表去获取学生信息
    stu = StuInfo.objects.filter(stu_age=27).first().stu
    # 2.通过学生表获取个人拓展表的信息
    stu_info = Student.objects.filter(id=3).first().stuinfo
    # 3.获取python班下的所有学生的信息和拓展表的信息
    stus = Grade.objects.filter(g_name='python').first().student_set
    stus_info = stus.first().stuinfo
    # 4.获取python班下语文成绩大于80分的女学生
    girls = Grade.objects.filter(g_name='python').first().\
        student_set.filter(Q(stu_shuxue__gt=80) & Q(stu_sex=0))
    # 5.获取python班下语文成绩超过数学成绩10分的男学生
    boys = Grade.objects.filter(g_name='python').first().\
        student_set.filter(stu_yuwen__gte=F('stu_shuxue') + 10).filter(stu_sex=1)
    # 6.获取出生在80后的男学生，查看他们的班级
    grade = Student.objects.filter(stu_birth__year__gte=1980).filter(stu_sex=1)
