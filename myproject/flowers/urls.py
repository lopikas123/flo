from django.urls import path
from . import views

app_name = 'flowers'

urlpatterns = [
    path('', views.flower_list, name='flower_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:flower_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/', views.order_confirmation, name='order_confirmation'),
]