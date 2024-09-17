from django.contrib import admin
from .models import Flower, Order, Review


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')
    search_fields = ('name', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('flower', 'user', 'delivery_address', 'delivery_date', 'delivery_time', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('flower__name', 'user__username', 'delivery_address')
    ordering = ('-created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['flower', 'user', 'rating', 'created_at']
    list_filter = ['flower', 'rating', 'created_at']