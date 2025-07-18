# Generated by Django 4.2.23 on 2025-06-29 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wb_id', models.IntegerField(unique=True, verbose_name='ID категории WB')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('url', models.URLField(verbose_name='URL')),
                ('shard', models.CharField(blank=True, max_length=100, verbose_name='Шард')),
                ('query', models.CharField(blank=True, max_length=255, verbose_name='Параметры запроса')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wb_id', models.BigIntegerField(unique=True, verbose_name='Артикул WB')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена')),
                ('discounted_price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена со скидкой')),
                ('rating', models.FloatField(blank=True, null=True, verbose_name='Рейтинг')),
                ('reviews_count', models.IntegerField(blank=True, null=True, verbose_name='Количество отзывов')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата парсинга')),
                ('url', models.URLField(verbose_name='Ссылка на товар')),
                ('brand', models.CharField(blank=True, max_length=255, null=True, verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['-created_at'],
            },
        ),
    ]
