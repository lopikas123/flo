import logging
from datetime import datetime
from django.forms import DurationField, FloatField
from django.core.management.base import BaseCommand
from django.db.models import Avg, Count, Func, ExpressionWrapper, F, fields



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot_token = "6387690359:AAGG4VTh5b4DV7yZDlHW-a_s-_H36wZToH4"



def report(update, context):
    report_data = generate_report()
    update.message.reply_text(report_data)

class Duration(Func):
    function = 'JULIANDAY'
    template = "%(function)s(%(expressions)s)"


def generate_report():
    from flowers.models import Order
    total_orders = Order.objects.count()
    average_order_amount = Order.objects.aggregate(Avg('price'))['price__avg']
    if average_order_amount is None:
        average_order_amount = 0.0

    orders = Order.objects.filter(status='out_for_delivery').exclude(delivery_date__isnull=True)

    total_delivery_time = 0
    delivered_orders_count = 0

    for order in orders:
        delivery_date = datetime.combine(order.delivery_date, datetime.min.time()) if order.delivery_date else None
        status_change_date = datetime.combine(order.status_change_date,
                                              datetime.min.time()) if order.status_change_date else None

        if delivery_date and status_change_date:
            delivery_duration = delivery_date - status_change_date
            duration_minutes = delivery_duration.total_seconds() / 60
            total_delivery_time += duration_minutes
            delivered_orders_count += 1

            # Отладочные выводы
            print(
                f"Order ID: {order.id}, Delivery Date: {delivery_date}, Status Change Date: {status_change_date}, Duration: {duration_minutes:.2f} minutes")

    if delivered_orders_count > 0:
        avg_delivery_time = total_delivery_time / delivered_orders_count
    else:
        avg_delivery_time = 0.0

    report_data = "Аналитика и отчеты по заказам:\n"
    report_data += f"Общее количество заказов: {total_orders}\n"
    report_data += f"Средняя сумма заказа: {average_order_amount:.2f}\n"
    report_data += f"Среднее время выполнения: {avg_delivery_time:.2f} минут\n"

    return report_data


class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **kwargs):
        from telegram import Update
        from telegram.ext import CommandHandler, CallbackContext, Updater

        updater = Updater(bot_token, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("report", report))
        updater.start_polling()
        updater.idle()



