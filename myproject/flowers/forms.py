from django import forms
from .models import Order,  Review



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Оставьте отзыв...'}),
            'rating': forms.Select(choices=[(i, f'{i} звезды') for i in range(1, 6)]),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['price', 'delivery_duration']  # Игнорируем эти поля
        fields = ['delivery_address', 'delivery_date', 'delivery_time', 'comment']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Order.STATUS_CHOICES)
        }


