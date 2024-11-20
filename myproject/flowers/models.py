from django.db import models

from django.contrib.auth.models import User

class Flower(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default='Описание отсутствует')
    image = models.ImageField(upload_to='flowers/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Принят к работе'),
        ('in_progress', 'Находится в работе'),
        ('out_for_delivery', 'В доставке'),
        ('completed', 'Выполнен'),
        ('canceled', 'Отмена')
    ]
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_duration = models.DurationField(null=True, blank=True)
    status_change_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Order {self.id} - {self.user} - {self.status}"



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart - {self.flower.name}"


class Review(models.Model):
    flower = models.ForeignKey(Flower, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user} on {self.flower}'

