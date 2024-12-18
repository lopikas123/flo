# Интернет-магазин цветов с интеграцией Telegram

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Описание

Этот проект представляет собой веб-сайт для управления интернет-магазином цветов с поддержкой аналитики и интеграцией с Telegram. Решение обеспечивает полный цикл управления заказами, включая регистрацию, каталог товаров, оплату, уведомления и аналитику.

---

## Функционал

### Веб-сайт
- **Авторизация**:
  - Регистрация и вход для разных ролей: покупатели, сотрудники, администраторы.
- **Каталог**:
  - Просмотр, фильтрация и добавление цветов в корзину.
  - Покупка с возможностью выбора доставки.
- **Оформление заказа**:
  - Управление корзиной.
  - Выбор метода доставки и оплаты.
- **Уведомления**:
  - Сотрудники получают уведомления о новых заказах через Telegram.
- **История заказов**:
  - Покупатели могут отслеживать свои заказы, включая их статус.
- **Изменение статуса заказов**:
  - Администраторы могут изменять статусы заказов.
  - Уведомления отправляются клиентам через Telegram и отображаются на сайте.
- **Аналитика**:
  - Владельцы могут просматривать отчеты о количестве заказов и выручке (в базе данных или отдельных документах).

### Telegram-бот
- **Уведомления**:
  - Отправка сообщений о новых заказах и изменениях их статусов сотрудникам и владельцам.
- **Аналитика**:
  - Бот предоставляет отчеты о выполненных заказах и финансовых результатах.

---

## Установка

### Требования
- Python 3.8+
- Django
- Telegram Bot API
- Сторонние библиотеки (указаны в `requirements.txt`).

## Шаги для установки

### 1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/lopikas123/flo.git
   cd flo/myproject
   ```
   
### 2. Установите зависимости:

      ```bash
   pip install -r requirements.txt
   ```

### 3. Настройте файл окружения .env с необходимыми параметрами:

- Настройки базы данных.
- Токен Telegram-бота.
- API ключи для платежной системы.

### 4. Выполните миграции базы данных:

      ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### 5. Запустите сервер разработки:

      ```bash
   python manage.py runserver
   ```

---

## Использование

### 1. Авторизация:
Зарегистрируйтесь как покупатель или войдите в систему.
### 2. Каталог:
Просмотрите доступные цветы и добавьте их в корзину.
### 3. Оформление заказа:
Завершите покупку, выбрав метод доставки и оплаты.
### 4. Администрирование:
Изменяйте статус заказов, отправляйте уведомления и просматривайте аналитику.

---

## Структура проекта

      ```bash
   MyProject/
├── accounts/             # Управление учетными записями
├── flowers/              # Модели и логика каталога
├── telegram_bot/         # Код для работы с Telegram API
├── analytics/            # Логика отчетности
├── static/               # Статические файлы
├── templates/            # HTML-шаблоны
├── manage.py             # Главный файл управления Django
└── requirements.txt      # Зависимости проекта
   ```

---

## Тестирование

Для запуска тестов используйте:

      ```bash
   python manage.py test
   ```

---

