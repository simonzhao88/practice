from django.conf.urls import url
from mytest import views


urlpatterns = [
    url(r'^test', views.test, name='test'),
]
