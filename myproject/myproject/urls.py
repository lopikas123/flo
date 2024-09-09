from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Представление для домашней страницы
def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Подключение приложения 'accounts'
    path('', home, name='home'),
]