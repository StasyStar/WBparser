import logging
import requests
import time
from urllib.parse import parse_qs

from django.core.management.base import BaseCommand
from products.models import Category, Product

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Парсинг товаров с Wildberries по выбранным категориям'

    def add_arguments(self, parser):
        parser.add_argument('--categories', nargs='+', type=int, help='ID категорий для парсинга')
        parser.add_argument('--pages', type=int, default=10, help='Количество страниц для парсинга')

    def handle(self, *args, **options):
        category_ids = options['categories']
        pages_to_parse = options['pages']

        if not category_ids:
            self.stdout.write(self.style.ERROR('Не указаны ID категорий'))
            return

        categories = Category.objects.filter(wb_id__in=category_ids, is_active=True)

        if not categories.exists():
            self.stdout.write(self.style.ERROR('Не найдено активных категорий'))
            return

        for category in categories:
            self.stdout.write(f"Парсинг категории: {category.name} (ID: {category.wb_id})")
            self.parse_category(category, pages_to_parse)

    def parse_category(self, category, pages=5):
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json',
        }

        query_params = parse_qs(category.query or '')
        cat_param_list = query_params.get('cat')
        if not cat_param_list:
            self.stdout.write(self.style.WARNING(f"Параметр 'cat' не найден в query категории {category.name}"))
            return
        cat_param = cat_param_list[0]

        base_url = f"https://catalog.wb.ru/catalog/{category.shard}/v2/catalog"

        for page in range(1, pages + 1):
            params = {
                'appType': 1,
                'curr': 'rub',
                'dest': '-1257786',
                'page': page,
                'sort': 'popular',
                'spp': 30,
                'cat': cat_param,
            }

            try:
                response = requests.get(base_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка запроса страницы {page} категории {category.name}: {e}"))
                break

            products = data.get('data', {}).get('products', [])
            if not products:
                self.stdout.write(f"Нет товаров на странице {page} категории {category.name}")
                break

            for product_data in products:
                try:
                    avg_basic_price, avg_discounted_price = self.calculate_avg_prices_from_sizes(product_data)

                    Product.objects.update_or_create(
                        wb_id=product_data['id'],
                        defaults={
                            'name': product_data.get('name', 'Без названия'),
                            'price': avg_basic_price,
                            'discounted_price': avg_discounted_price,
                            'rating': product_data.get('rating'),
                            'reviews_count': product_data.get('feedbacks', 0),
                            'category': category,
                            'url': f"https://www.wildberries.ru/catalog/{product_data['id']}/detail.aspx",
                            'brand': product_data.get('brand', '')
                        }
                    )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Ошибка при сохранении товара {product_data.get('id')}: {e}"))

            time.sleep(1)

    @staticmethod
    def calculate_avg_prices_from_sizes(product_data):
        sizes = product_data.get('sizes', [])
        basic_prices = []
        discounted_prices = []

        for size in sizes:
            if isinstance(size, dict):
                price_info = size.get('price')
                if isinstance(price_info, dict):
                    basic = price_info.get('basic', 0)    # цена без скидки
                    discounted = price_info.get('product', basic)  # цена со скидкой, fallback на basic если нет
                    if basic > 0:
                        basic_prices.append(basic)
                    if discounted > 0:
                        discounted_prices.append(discounted)

        if not basic_prices:
            avg_basic = 0
        else:
            avg_basic = sum(basic_prices) / len(basic_prices)

        if not discounted_prices:
            avg_discounted = avg_basic
        else:
            avg_discounted = sum(discounted_prices) / len(discounted_prices)

        # Переводим из копеек в рубли с двумя знаками после запятой
        return round(avg_basic / 100, 2), round(avg_discounted / 100, 2)
