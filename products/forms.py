from django import forms
from .models import Category


class CategorySelectForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'category-checkbox'}),
        label="Выберите категории для парсинга"
    )
