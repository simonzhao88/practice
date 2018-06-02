from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from rest_framework.response import Response

from stu.filters import StudentFilter
from stu.serializer import StudentSerializer, GradeSerializer
from utils.check_login import is_login
from stu.models import Grade, Student
from rest_framework import mixins, viewsets
import logging
logger = logging.getLogger('console')


def index(request):
    """
    首页
    :param request:
    :return:
    """
    if request.method == 'GET':
        logger.info('获取到了首页')
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
    # if request.method == 'GET':
    #     page_num = request.GET.get('page_num', 1)
    #     grades = Grade.objects.all()
    #     paginator = Paginator(grades, 3)
    #     pages = paginator.page(int(page_num))
    #     ctx = {
    #         'pages': pages,
    #         'page_num': page_num
    #     }
    #     return render(request, 'grade.html', context=ctx)
    return render(request, 'grade.html')


def add_grade(request):
    """
    渲染班级添加页面及实现添加班级
    修改班级页面渲染及实现修改班级
    :param request:
    :return:
    """
    # gid = int(request.GET.get('id'))
    # if request.method == 'GET':
    #     if gid == 0:
    #         return render(request, 'addgrade.html')
    #     else:
    #         ctx = {
    #             'grade': Grade.objects.get(id=gid)
    #         }
    #         return render(request, 'addgrade.html', context=ctx)
    # g_name = request.POST.get('grade_name')
    # if gid == 0:
    #     g = Grade()
    #     g.g_name = g_name
    #     g.save()
    # else:
    #     g = Grade.objects.filter(id=gid).first()
    #     g.g_name = g_name
    #     g.save()
    # return redirect('stu:grade')
    if request.method == 'GET':
        return render(request, 'addgrade.html')
    # 若是HttpResponseRedirect则要导入reverse()方法


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


def student(request):
    """
    学生界面
    :param request:
    :return:
    """
    # if request.method == 'GET':
    #     page_num = request.GET.get('page_num', 1)
    #     stus = Student.objects.filter(delete=0)
    #     paginator = Paginator(stus, 3)
    #     pages = paginator.page(int(page_num))
    #     ctx = {
    #         'pages': pages,
    #         'page_num': page_num
    #     }
    #     return render(request, 'student.html', context=ctx)
    return render(request, 'student.html')


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


class ApiStudent(mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin, viewsets.GenericViewSet,):

    # 学生的所有信息
    queryset = Student.objects.all().filter(delete=False)
    # 序列化学生的所有信息（过滤）
    serializer_class = StudentSerializer
    # 配置过滤规则
    filter_class = StudentFilter

    def perform_destroy(self, instance):
        """
        重写删除方法，使成为软删除
        :param instance:
        :return:
        """
        instance.delete = True
        instance.save()

    def get_queryset(self):

        # query = self.queryset
        # s_name = self.request.query_params.get('s_name')
        return self.queryset.order_by('-id')


class ApiGrade(mixins.ListModelMixin, mixins.CreateModelMixin,
               mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
               mixins.UpdateModelMixin, viewsets.GenericViewSet,):

    queryset = Grade.objects.filter(delete=False)

    serializer_class = GradeSerializer

    def perform_destroy(self, instance):
        """
        重写删除方法，使成为软删除
        :param instance:
        :return:
        """
        instance.delete = True
        instance.save()

    def update(self, request, *args, **kwargs):
        """
        重写update方法完成修改，其他方法也是如此
        自定义code状态码和msg消息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.do_update(instance, request.data)
        data = serializer.data
        data['code'] = 200
        data['msg'] = '修改班级成功'
        return Response(data)


def badpage404(request):
    return render(request, '404.html')