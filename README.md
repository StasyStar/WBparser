# 🛍️ WBParser

Проект для парсинга товаров с Wildberries, анализа и отображения данных с возможностью фильтрации и сортировки.

## 📊 Функционал
- Парсинг товаров по выбранным категориям с Wildberries API
- Автоматическое обновление данных при необходимости
- Фильтрация товаров по категории, цене (двойной слайдер), минимальному рейтингу и количеству отзывов
- Сортировка товаров по дате, цене и рейтингу
- Пагинация списка товаров
- Визуализация данных с помощью графиков: распределение цен и зависимость скидки от рейтинга
- Удобный веб-интерфейс с Bootstrap


## 💻 Использованные технологии
- Python 3 + Django (веб-фреймворк)
- requests (HTTP-запросы для парсинга)
- matplotlib, numpy (построение графиков)
- Bootstrap 5 (стилизация и UI)
- noUiSlider (двойной слайдер для выбора диапазона цены)

## 🚀 Установка

```bash
# Клонируем проект
git clone https://github.com/your-username/wbparser.git
cd wbparser

# Создаем и активируем виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate  # Для Windows: .venv\Scripts\activate

# Устанавливаем зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Применяем миграции
python manage.py migrate

# Загружаем категории Wildberries
python manage.py load_wb_categories

# Запускаем сервер разработки
python manage.py runserver
