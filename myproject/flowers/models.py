from django.db import models

class Flower(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class CartItem(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.flower.price * self.quantity

    def __str__(self):
        return f'{self.flower.name} - {self.quantity}'