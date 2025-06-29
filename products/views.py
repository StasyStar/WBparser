from django.shortcuts import render
from django.views import View
from products.models import Product, Category
from django.contrib import messages
import subprocess
from django.utils import timezone
from products.utils import generate_price_histogram, generate_discount_rating_chart
from django.core.paginator import Paginator
from django.db.models import Min, Max


class ProductListView(View):
    def get(self, request):
        category_id = request.GET.get('category')
        sort = request.GET.get('sort', '-created_at')
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        min_rating = request.GET.get('min_rating')
        min_reviews = request.GET.get('min_reviews')

        # Проверяем, когда последний раз парсилась категория
        if category_id:
            category = Category.objects.get(id=category_id)
            last_parsed = Product.objects.filter(
                category=category
            ).order_by('-created_at').first()

            if not last_parsed or (timezone.now() - last_parsed.created_at).days > 1:
                messages.info(request, f'Обновляем данные для категории: {category.name}')
                subprocess.Popen([
                    'python', 'manage.py', 'parse_wb_products',
                    '--categories', str(category.wb_id),
                    '--pages', '3'
                ])

        # Фильтрация товаров
        products = Product.objects.all()
        if category_id:
            products = products.filter(category_id=category_id)

        # Получаем минимальную и максимальную цену для слайдера (по текущему фильтру категории)
        price_range = products.aggregate(min_price=Min('discounted_price'), max_price=Max('discounted_price'))
        min_price_db = price_range['min_price'] or 0
        max_price_db = price_range['max_price'] or 100000

        # Устанавливаем значения фильтра цены, либо по умолчанию из базы
        try:
            price_from_val = float(price_from) if price_from is not None else min_price_db
        except ValueError:
            price_from_val = min_price_db

        try:
            price_to_val = float(price_to) if price_to is not None else max_price_db
        except ValueError:
            price_to_val = max_price_db

        # Ограничиваем фильтрацию по цене в пределах базы
        if price_from_val < min_price_db:
            price_from_val = min_price_db
        if price_to_val > max_price_db:
            price_to_val = max_price_db

        products = products.filter(discounted_price__gte=price_from_val, discounted_price__lte=price_to_val)

        if min_rating:
            try:
                products = products.filter(rating__gte=float(min_rating))
            except ValueError:
                pass

        if min_reviews:
            try:
                products = products.filter(reviews_count__gte=int(min_reviews))
            except ValueError:
                pass

        products = products.order_by(sort)

        paginator = Paginator(products, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'categories': Category.objects.filter(is_active=True),
            'products': page_obj,
            'price_histogram': generate_price_histogram(products),
            'discount_rating_chart': generate_discount_rating_chart(products),
            'current_category': int(category_id) if category_id else None,
            'sort': sort,
            'min_price': int(min_price_db),
            'max_price': int(max_price_db),
            'price_from': int(price_from_val),
            'price_to': int(price_to_val),
            'min_rating': min_rating,
            'min_reviews': min_reviews,
        }
        return render(request, 'products.html', context)
