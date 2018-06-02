"""
功能：继承过滤类，自定义过滤规则
author：simon
"""

import django_filters

from rest_framework import filters

from stu.models import Student


class StudentFilter(filters.FilterSet):
    # 实现姓名模糊查询
    s_name = django_filters.CharFilter('s_name', lookup_expr='contains')

    class Meta:
        model = Student
        fields = ['s_name', ]
