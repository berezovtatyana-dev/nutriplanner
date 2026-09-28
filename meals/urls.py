from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/<int:product_id>/', views.add_to_plan, name='add_to_plan'),
    path('my_plan/', views.meal_plan_detail, name='meal_detail_plan'),
    path('remove/<int:product_id>/', views.remove_from_plan, name='remove_from_plan'),
    path('clear/', views.clear_plan, name='clear_plan'),
]