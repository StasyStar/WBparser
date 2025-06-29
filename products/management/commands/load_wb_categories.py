import requests
from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Загрузка категорий с Wildberries'

    def handle(self, *args, **options):
        url = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json"

        try:
            response = requests.get(url)
            response.raise_for_status()
            categories_data = response.json()

            # Сначала создаем родительские категории
            for item in categories_data:
                if 'childs' in item:
                    try:
                        parent_category, _ = Category.objects.get_or_create(
                            wb_id=item['id'],
                            defaults={
                                'name': item['name'],
                                'url': f"https://www.wildberries.ru{item['url']}",
                                'shard': item.get('shard', ''),
                                'query': item.get('query', ''),
                                'is_active': True
                            }
                        )
                        # Затем обрабатываем дочерние категории
                        if 'childs' in item:
                            self.parse_child_categories(item['childs'], parent_category)
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'Ошибка при обработке родительской категории {item.get("name")}: {e}'))

            self.stdout.write(self.style.SUCCESS('Категории успешно загружены'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))

    def parse_child_categories(self, childs, parent):
        for child in childs:
            try:
                Category.objects.get_or_create(
                    wb_id=child['id'],
                    defaults={
                        'name': child['name'],
                        'parent': parent,
                        'url': f"https://www.wildberries.ru{child['url']}",
                        'shard': child.get('shard', ''),
                        'query': child.get('query', ''),
                        'is_active': True
                    }
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Ошибка при обработке дочерней категории {child.get("name")}: {e}'))
