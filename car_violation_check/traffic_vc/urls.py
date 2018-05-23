from django.conf.urls import url
from traffic_vc import views

urlpatterns = [
    url('traffic_check', views.index, name='index'),
    url('showrecord', views.showrecord, name='showrecord')
]
