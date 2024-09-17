
from datetime import timedelta
import requests
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Sum

from .models import Flower, Cart, Order
from .forms import OrderForm, OrderStatusForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .config import bot_token, chat_id



def flower_catalog(request):
    flowers = Flower.objects.filter(available=True)
    return render(request, 'flower_catalog.html', {'flowers': flowers})

def cart_view(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, flower=flower)

    if not created:
        # If the item already exists, just increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')



@login_required
def create_order(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)  # Получаем цветок по id

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.flower = flower
            order.user = request.user
            order.price = flower.price  # Устанавливаем цену на основе модели Flower
            order.save()

            # Подготовка сообщения для Telegram
            message = (
                f"Новый заказ:\n\n"
                f"Номер заказа: {order.id}\n"
                f"Заказчик: {request.user.username}\n"
                f"Цветок: {flower.name}\n"
                f"Адрес доставки: {order.delivery_address}\n"
                f"Дата доставки: {order.delivery_date}\n"
                f"Время доставки: {order.delivery_time}\n"
                f"Комментарий: {order.comment}\n"
                f"Цена: {order.price} руб.\n"
                f"Статус: {order.get_status_display()}"
            )

            # Отправка сообщения в Telegram
            image_url = request.build_absolute_uri(flower.image.url) if flower.image else None

            try:
                if image_url:
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        send_message_url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
                        response = requests.post(send_message_url, data={
                            'chat_id': chat_id,
                            'caption': message
                        }, files={
                            'photo': ('flower_image.jpg', image_response.content)
                        })
                    else:
                        return HttpResponse("Ошибка при загрузке изображения.", status=500)
                else:
                    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
                    response = requests.post(send_message_url, data={
                        'chat_id': chat_id,
                        'text': message
                    })

                if response.status_code == 200:
                    return redirect('order_history')  # Перенаправляем на историю заказов
                else:
                    return HttpResponse(
                        f"Ошибка при отправке данных в Telegram. Код ошибки: {response.status_code}. Ответ: {response.text}",
                        status=500)

            except requests.RequestException as e:
                return HttpResponse(f"Произошла ошибка при отправке запроса: {str(e)}", status=500)

    else:
        form = OrderForm()

    return render(request, 'create_order.html', {'flower': flower, 'form': form})




@login_required
def order_history(request):
    # Получаем заказы пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


def is_superuser(user):
    return user.is_superuser


@login_required
def order_history(request):
    if request.user.is_superuser:
        orders = Order.objects.all()  # Показываем все заказы для суперпользователя
    else:
        orders = Order.objects.filter(user=request.user)  # Показываем только заказы текущего пользователя

    return render(request, 'order_history.html', {'orders': orders})



@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Check if the user is a superuser
    if not request.user.is_superuser:
        return redirect('order_history')  # Redirect non-superusers to order history

    previous_status = order.status  # Store the current status for comparison

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()  # Save the form data
            new_status = form.cleaned_data['status']  # Get the new status

            if previous_status != new_status:  # Check if the status has changed
                # Prepare the message for Telegram
                message = (f"Статус заказа #{order.id} изменён с "
                           f"{dict(Order.STATUS_CHOICES).get(previous_status)} на "
                           f"{dict(Order.STATUS_CHOICES).get(new_status)}")



                url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
                payload = {
                    'chat_id': chat_id,
                    'text': message
                }

                try:
                    # Send the message to Telegram
                    response = requests.post(url, data=payload)
                    response.raise_for_status()  # Raise an exception for HTTP errors
                except requests.RequestException as e:
                    # Handle request errors (e.g., log the error or notify the admin)
                    print(f"Error sending message to Telegram: {e}")

            messages.success(request, f'Статус заказа #{order.id} был обновлён.')
            return redirect('order_history')
    else:
        form = OrderStatusForm(instance=order)  # Provide the form with the current order data

    # Render the form in the template
    return render(request, 'update_status.html', {'form': form, 'order': order})

@login_required
def repair_order(request, order_id):
    # Получаем исходный заказ
    original_order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Создаем новый заказ на основе данных исходного заказа
            new_order = Order.objects.create(
                flower=original_order.flower,
                delivery_address=form.cleaned_data['delivery_address'],
                delivery_date=form.cleaned_data['delivery_date'],
                delivery_time=form.cleaned_data['delivery_time'],
                comment=form.cleaned_data['comment'],
                price=original_order.price,
                status='Принят к работе',  # Устанавливаем новый статус для повторного заказа
                user=request.user  # Присваиваем новый заказ текущему пользователю
            )

            # Создание сообщения для Telegram
            message = (
                f"Новый заказ (повторный):\n\n"
                f"Заказчик: {request.user.username}\n"
                f"Цветок: {new_order.flower.name}\n"
                f"Адрес доставки: {new_order.delivery_address}\n"
                f"Дата доставки: {new_order.delivery_date}\n"
                f"Время доставки: {new_order.delivery_time}\n"
                f"Комментарий: {new_order.comment}\n"
                f"Цена: {new_order.price} руб.\n"
                f"Статус: {new_order.get_status_display()}"
            )



            image_url = request.build_absolute_uri(new_order.flower.image.url) if new_order.flower.image else None
            try:
                if image_url:
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        send_message_url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
                        response = requests.post(send_message_url, data={
                            'chat_id': chat_id,
                            'caption': message
                        }, files={
                            'photo': ('flower_image.jpg', image_response.content)
                        })
                    else:
                        return HttpResponse("Ошибка при загрузке изображения.", status=500)
                else:
                    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
                    response = requests.post(send_message_url, data={
                        'chat_id': chat_id,
                        'text': message
                    })

                if response.status_code == 200:
                    return redirect('order_history')
                else:
                    return HttpResponse(f"Ошибка при отправке данных в Telegram. Код ошибки: {response.status_code}. Ответ: {response.text}", status=500)

            except requests.RequestException as e:
                return HttpResponse(f"Произошла ошибка при отправке запроса: {str(e)}", status=500)

    else:
        form = OrderForm(initial={
            'delivery_address': original_order.delivery_address,
            'delivery_date': original_order.delivery_date,
            'delivery_time': original_order.delivery_time,
            'comment': original_order.comment,
        })

    return render(request, 'repair_order.html', {'form': form})


@login_required
def add_review(request, flower_id):
    flower = Flower.objects.get(id=flower_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.flower = flower
            review.user = request.user
            review.save()
            return redirect('flower_detail', flower_id=flower.id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'flower': flower, 'form': form})

def flower_detail(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    reviews = flower.reviews.all()

    return render(request, 'flower_detail.html', {'flower': flower, 'reviews': reviews})

@user_passes_test(is_superuser)
def daily_report(request):
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Сбор данных по дням
    days_range = [first_day_of_month + timedelta(days=i) for i in range((last_day_of_month - first_day_of_month).days + 1)]
    daily_reports = []

    for day in days_range:
        orders_day = Order.objects.filter(created_at__date=day)
        total_orders_day = orders_day.count()
        total_revenue_day = orders_day.aggregate(total_revenue=Sum('price'))['total_revenue'] or 0

        daily_reports.append({
            'date': day,
            'total_orders': total_orders_day,
            'total_revenue': total_revenue_day
        })

    # Общие данные за месяц
    orders_month = Order.objects.filter(created_at__date__range=[first_day_of_month, last_day_of_month])
    total_orders_month = orders_month.count()
    total_revenue_month = orders_month.aggregate(total_revenue=Sum('price'))['total_revenue'] or 0

    context = {
        'daily_reports': daily_reports,
        'total_orders_month': total_orders_month,
        'total_revenue_month': total_revenue_month,
        'month': first_day_of_month.strftime('%B %Y')  # Например: "Сентябрь 2024"
    }

    # Генерация HTML-контента
    html_content = render_to_string('daily_report.html', context)

    # Создание HTTP-ответа
    response = HttpResponse(html_content, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="daily_report_{today.strftime("%Y-%m")}.html"'

    return response


