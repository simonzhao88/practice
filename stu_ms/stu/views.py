from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from utils.check_login import is_login
from stu.models import Grade, Student


@is_login
def index(request):
    """
    首页
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'index.html')


@is_login
def head(request):
    """
    首页头部
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'head.html')


@is_login
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


@is_login
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


@is_login
def add_grade(request):
    """
    渲染班级添加页面及实现添加班级
    修改班级页面渲染及实现修改班级
    :param request:
    :return:
    """
    gid = int(request.GET.get('id'))
    if request.method == 'GET':
        if gid == 0:
            return render(request, 'addgrade.html')
        else:
            ctx = {
                'grade': Grade.objects.get(id=gid)
            }
            return render(request, 'addgrade.html', context=ctx)
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


@is_login
def del_grade(request):
    """
    实现删除班级
    :param request:
    :return:
    """
    if request.method == 'GET':
        gid = request.GET.get('id')
        Grade.objects.filter(id=gid).delete()
        return redirect('stu:grade')


@is_login
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


@is_login
def add_stu(request):
    """
    渲染添加学生页面及实现添加学生
    :param request:
    :return:
    """
    sid = int(request.GET.get('id'))
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
    s_name = request.POST.get('stu_name')
    g_id = request.POST.get('g_id')
    s_img = request.FILES.get('s_img')
    g = Grade.objects.filter(id=g_id).first()
    if sid == 0:
        Student.objects.create(s_name=s_name, g=g, s_img=s_img)
    else:
        s = Student.objects.get(id=sid)
        s.s_name = s_name
        s.g = g
        s.s_img = s_img
        s.save()
    return redirect('stu:student')


@is_login
def del_stu(request):
    """
    实现删除学生
    :param request:
    :return:
    """
    if request.method == 'GET':
        sid = request.GET.get('id')
        Student.objects.filter(id=sid).delete()
        return redirect('stu:student')
