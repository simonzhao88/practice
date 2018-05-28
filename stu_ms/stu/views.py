from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from stu.models import Grade, Student


def index(request):
    """
    首页
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'index.html')


def head(request):
    """
    首页头部
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'head.html')


def left(request):
    """
    首页左部
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'left.html')


def main(request):
    if request.method == 'GET':
        return render(request, 'main.html')


def grade(request):
    """
    首页grade页面
    :param request:
    :return:
    """
    if request.method == 'GET':
        page_num = request.GET.get('page_num', 1)
        grades = Grade.objects.all()
        paginator = Paginator(grades, 3)
        pages = paginator.page(int(page_num))
        ctx = {
            'pages': pages,
            'page_num': page_num
        }
        return render(request, 'grade.html', context=ctx)


def add_grade(request, gid=0):
    """
    渲染班级添加页面及实现添加班级
    修改班级页面渲染及实现修改班级
    :param request:
    :param gid:
    :return:
    """
    gid = int(gid)
    if request.method == 'GET':
        if gid == 0:
            return render(request, 'addgrade.html')
        else:
            ctx = {
                'grade': Grade.objects.get(id=gid)
            }
            return render(request, 'addgrade.html', context=ctx)
    if request.method == 'POST':
        g_name = request.POST.get('grade_name')
        if gid == 0:
            g = Grade()
            g.g_name = g_name
            g.save()
        else:
            g = Grade.objects.filter(id=gid).first()
            g.g_name = g_name
            g.save()
        return redirect('stu:grade')
    # 若是HttpResponseRedirect则要导入reverse()方法


def del_grade(request, gid):
    """
    实现删除班级
    :param request:
    :param gid:
    :return:
    """
    if request.method == 'POST':
        Grade.objects.filter(id=gid).delete()
        return redirect('stu:grade')


def student(request):
    """
    学生界面
    :param request:
    :return:
    """
    if request.method == 'GET':
        page_num = request.GET.get('page_num', 1)
        stus = Student.objects.all()
        paginator = Paginator(stus, 3)
        pages = paginator.page(int(page_num))
        ctx = {
            'pages': pages,
            'page_num': page_num
        }
        return render(request, 'student.html', context=ctx)


def add_stu(request, sid):
    """
    渲染添加学生页面及实现添加学生
    :param request:
    :return:
    """
    sid = int(sid)
    if request.method == 'GET':
        if sid == 0:
            ctx = {
                'grades': Grade.objects.all()
            }
        else:
            ctx = {
                'stu': Student.objects.get(id=sid),
                'grades': Grade.objects.all()
            }
        return render(request, 'addstu.html', context=ctx)
    if request.method == 'POST':
        s_name = request.POST.get('stu_name')
        g_id = request.POST.get('g_id')
        g = Grade.objects.filter(id=g_id).first()
        if sid == 0:
            Student.objects.create(s_name=s_name, g=g)
        else:
            s = Student.objects.get(id=sid)
            s.s_name = s_name
            s.g = g
            s.save()
        return redirect('stu:student')


def del_stu(request, sid):
    """
    实现删除学生
    :param request:
    :param sid:
    :return:
    """
    if request.method == 'POST':
        Student.objects.filter(id=sid).delete()
        return redirect('stu:student')
