import copy
from json import dumps, loads, JSONEncoder

from django import forms
# from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from traffic_vc.models import Trecord


def index(request):
    return render(request, 'index.html')


class CarRecordEncoder(JSONEncoder):

    def default(self, o):
        co = copy.deepcopy(o)
        del co.__dict__['_state']
        del co.__dict__['_django_version']
        co.__dict__['v_date'] = co.happen_date
        print(co.__dict__)
        return co.__dict__


def showrecord(request):
    content = request.POST['content']
    # record_set = Trecord.objects.filter(lic_plate__contains=content)
    record_list = list(Trecord.objects.filter(lic_plate__icontains=content))
    if record_list:
        return JsonResponse(record_list, encoder=CarRecordEncoder, safe=False)
        # 第一个参数是要转换成JSON格式（序列化的对象）
        # 第二个参数encoder参数要指定完成自定义对象序列化的编码器（JSONEncoder）的子类
        # safe参数的值如果为Truename传入的第一个采纳数只能是字典
        # record_lists = loads(serializers.serialize('json', record_set, ensure_ascii=False))
        # return HttpResponse(dumps(record_lists), content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('{}')


class CarRecordForm(forms.Form):
    no = forms.CharField(min_length=12, max_length=12, label='编号')
    lic_plate = forms.CharField(min_length=7, max_length=7, label='车牌号', error_messages={'err': '请输入正确的车牌'})
    reason = forms.CharField(max_length=100, label='违章原因')
    punishment = forms.CharField(max_length=100, label='处罚方式', required=False)


def add_record(request):
    errors = []
    if request.method == 'GET':
        f = CarRecordForm()
    else:
        f = CarRecordForm(request.POST)
        if f.is_valid():
            Trecord(**f.cleaned_data).save()
            f = CarRecordForm()
        else:
            errors = f.errors.values()
    return render(request, 'addrecord.html', {'f': f, 'errors': errors})
