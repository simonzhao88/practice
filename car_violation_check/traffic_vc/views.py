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
        print(record_lists)
        return HttpResponse(dumps(record_lists), content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('')
