# Generated by Django 5.1.1 on 2024-09-17 19:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(default='Описание отсутствует')),
                ('image', models.ImageField(blank=True, null=True, upload_to='flowers/')),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('flower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowers.flower')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_address', models.CharField(max_length=255)),
                ('delivery_date', models.DateField()),
                ('delivery_time', models.TimeField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Принят к работе'), ('in_progress', 'Находится в работе'), ('out_for_delivery', 'В доставке'), ('completed', 'Выполнен'), ('canceled', 'Отмена')], default='pending', max_length=20)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('delivery_duration', models.DurationField(blank=True, null=True)),
                ('status_change_date', models.DateTimeField(auto_now=True)),
                ('flower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowers.flower')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('flower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='flowers.flower')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
