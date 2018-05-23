from json import dumps, loads

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from traffic_vc.models import Trecord


def index(request):
    return render(request, 'index.html')


def showrecord(request):
    content = request.POST['content']
    record_set = Trecord.objects.filter(lic_plate__contains=content)
    if record_set:
        record_lists = loads(serializers.serialize('json', record_set, ensure_ascii=False))
        record_list = []
        for records in record_lists:
            record_list.append(records['fields'])
        print(record_list)
        ctx = {
            'records': record_list
        }
        print(dumps(ctx, ensure_ascii=False))
        return HttpResponse(dumps(ctx), content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('{}')
