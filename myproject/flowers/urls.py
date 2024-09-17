from django.urls import path
from . import views


urlpatterns = [
    path('', views.flower_catalog, name='flower_catalog'),
    path('create_order/<int:flower_id>/', views.create_order, name='create_order'),
    path('order-history/', views.order_history, name='order_history'),
    path('<int:order_id>/update/', views.update_order_status, name='update_status'),
    path('repair/<int:order_id>/', views.repair_order, name='repair_order'),
    path('flower/<int:flower_id>/', views.flower_detail, name='flower_detail'),
    path('flower/<int:flower_id>/add_review/', views.add_review, name='add_review'),
    path('daily_report/', views.daily_report, name='daily_report'),




]