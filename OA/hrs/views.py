from datetime import datetime
from random import randrange

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
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


def emps(request):
    try:
        dno = request.GET['dno']
    except:
        dno = ''
    if dno:
        ctx = {
            'emps': Emp.objects.filter(dept_id=dno)
        }
    else:
        ctx = {
            'emps': Emp.objects.all()
        }
    return render(request, 'emp.html', context=ctx)


def deldept(request):
    dno = request.POST['dno']
    try:
        Dept.objects.filter(no=dno).delete()
        return HttpResponse('1')
    except BaseException:
        return HttpResponse('0')

