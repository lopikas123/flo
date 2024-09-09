from django.shortcuts import render, redirect, get_object_or_404
from .models import Flower, CartItem

# Просмотр каталога цветов
def flower_list(request):
    flowers = Flower.objects.all()
    return render(request, 'flowers/flower_list.html', {'flowers': flowers})

# Добавление цветка в корзину
def add_to_cart(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    cart_item, created = CartItem.objects.get_or_create(flower=flower)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

# Просмотр корзины
def view_cart(request):
    cart_items = CartItem.objects.all()
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

# Оформление заказа (страница оформления)
def checkout(request):
    cart_items = CartItem.objects.all()
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})

# Подтверждение заказа
def order_confirmation(request):
    CartItem.objects.all().delete()  # Очистка корзины после подтверждения
    return render(request, 'order_confirmation.html')