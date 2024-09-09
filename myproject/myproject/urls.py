from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # Импортируем redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flowers/', include('flowers.urls')),  # Подключение приложения 'flowers'
    path('accounts/', include('accounts.urls')),  # Подключение приложения 'accounts'
    path('', lambda request: redirect('flower_list')),  # Перенаправление на каталог цветов
]