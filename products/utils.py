import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from io import BytesIO
import base64
import numpy as np


def generate_price_histogram(queryset):
    prices = [p.price for p in queryset if p.price is not None]

    if not prices:
        return None

    plt.figure(figsize=(10, 6))
    plt.hist(prices, bins=20, edgecolor='black')
    plt.title('Распределение цен')
    plt.xlabel('Цена (руб)')
    plt.ylabel('Количество товаров')
    plt.grid(True, alpha=0.3)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')


def generate_discount_rating_chart(queryset):
    data = [(p.rating, p.discount) for p in queryset if p.rating is not None and p.discount is not None]

    if not data:
        return None

    ratings, discounts = zip(*data)

    plt.figure(figsize=(10, 6))
    plt.scatter(ratings, discounts, alpha=0.5)
    plt.title('Зависимость скидки от рейтинга')
    plt.xlabel('Рейтинг')
    plt.ylabel('Скидка (%)')
    plt.grid(True, alpha=0.3)

    try:
        z = np.polyfit(ratings, discounts, 1)
        p = np.poly1d(z)
        sorted_ratings = sorted(ratings)
        plt.plot(sorted_ratings, p(sorted_ratings), "r--")
    except Exception:
        pass

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')


