from django.db import models


class Category(models.Model):
    wb_id = models.IntegerField(unique=True, verbose_name="ID категории WB")
    name = models.CharField(max_length=255, verbose_name="Название")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Родительская категория")
    url = models.URLField(verbose_name="URL")
    shard = models.CharField(max_length=100, blank=True, verbose_name="Шард")
    query = models.CharField(max_length=255, blank=True, verbose_name="Параметры запроса")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    wb_id = models.BigIntegerField(unique=True, verbose_name="Артикул WB")
    name = models.CharField(max_length=500, verbose_name="Название")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    discounted_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена со скидкой")
    rating = models.FloatField(null=True, blank=True, verbose_name="Рейтинг")
    reviews_count = models.IntegerField(null=True, blank=True, verbose_name="Количество отзывов")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата парсинга")
    url = models.URLField(verbose_name="Ссылка на товар")
    brand = models.CharField(max_length=255, null=True, blank=True, verbose_name="Бренд")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.name} ({self.wb_id})"

    @property
    def discount(self):
        return round((1 - self.discounted_price / self.price) * 100, 2) if self.price and self.discounted_price else 0

    def get_price(self):
        return f"{self.price:.2f} ₽" if self.price else "Нет цены"

    def get_discounted_price(self):
        return f"{self.discounted_price:.2f} ₽" if self.discounted_price else self.get_price()

    def get_discount(self):
        if self.price and self.discounted_price and self.price > 0:
            discount = ((self.price - self.discounted_price) / self.price) * 100
            return f"-{discount:.0f}%"
        return ""
