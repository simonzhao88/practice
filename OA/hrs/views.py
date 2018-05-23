from datetime import datetime
from json import dumps
from random import randrange

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse

from hrs.models import Dept, Emp


def home(request):
    # html = '北京时间：%s' % datetime.now()
    # return HttpResponse(html)
    fruit_list = ['香蕉', '苹果', '橘子', '蓝莓', '梨', '红提']
    end = randrange(1, len(fruit_list))
    fruits = fruit_list[0:end]
    context = {
        'greeting': '你好, 世界!',
        'current_time': datetime.now(),
        'num': len(fruits),
        'fruits': fruits
    }
    return render(request, 'index.html', context=context)


def depts(request):
    ctx = {'depts': Dept.objects.all()}
    return render(request, 'dept.html', context=ctx)


def emps(request, dno=0):
    if dno:
        emps_list = Emp.objects.filter(dept__no=dno).select_related('dept')
        ctx = {
            'emps': emps_list,
            'dept_name': emps_list[0].dept}\
            if len(emps_list) > 0 else \
            {'dept_name': Dept.objects.get(no=dno).name}
    else:
        ctx = {
            'emps': Emp.objects.all(),
            'dept_name': '全部'
        }
    return render(request, 'emp.html', context=ctx)


def deldept(request):
    dno = request.POST['dno']
    try:
        Dept.objects.filter(no=dno).delete()
        return HttpResponse('1')
    except BaseException:
        return HttpResponse('0')


def delemp(request):
    try:
        eno = request.POST['eno']
        Emp.objects.get(no=eno).delete()
        ctx = {'code': 200}
        return HttpResponse(dumps(ctx), content_type='application/json; charset=utf-8')
    except (ValueError, ObjectDoesNotExist):
        ctx = {'code': 404}
        return HttpResponse(dumps(ctx), content_type='application/json; charset=utf-8')

