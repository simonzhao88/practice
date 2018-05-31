from django.conf.urls import url
from stu import views


from rest_framework.routers import SimpleRouter

router = SimpleRouter()
# 注册rest路由
router.register(r'^api/student', views.ApiStudent)
router.register(r'^api/grade', views.ApiGrade)

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^head/', views.head, name='head'),
    url(r'^left/', views.left, name='left'),
    url(r'^main/', views.main, name='main'),
    url(r'^grade/', views.grade, name='grade'),
    url(r'^addgrade/', views.add_grade, name='addgrade'),
    url(r'^student/', views.student, name='student'),
    url(r'^addstu/', views.add_stu, name='addstu'),
    url(r'^editgrade/', views.add_grade, name='editgrade'),
    url(r'^delgrade/', views.del_grade, name='delgrade'),
    url(r'^editstu/', views.add_stu, name='editstu'),
    url(r'^delstu/', views.del_stu, name='delstu'),

]

# 使定义的rest风格的url生效
urlpatterns += router.urls
