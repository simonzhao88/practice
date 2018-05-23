from django.urls import path

from hrs import views

urlpatterns = [
    path('depts/', views.depts, name='depts'),
    path('emps/<int:dno>', views.emps, name='emps'),
    path('deldept', views.deldept, name='deldept'),
    path('delemp', views.delemp, name='delemp'),
]