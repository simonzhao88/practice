from cart import views

from django.urls import path

urlpatterns = [
    path('', views.index),
    path('add_to_cart/<int:id>', views.add_to_cart),
    path('show_cart', views.show_cart),
    path('del_good/<int:id>', views.del_good),
    path('clear_cart', views.clear_cart),
    path('dev_amount/<int:id>', views.dev_amount),
    path('add_amount/<int:id>', views.add_amount),
]
