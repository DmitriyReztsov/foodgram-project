from django import forms
from django.contrib.auth import get_user_model

from .models import Recipe

User = get_user_model()


class RecipeForm(forms.ModelForm):
    """Создаем класс формы на базе модели Recipe
       для добавления в Post новых записей"""
    class Meta:
        model = Recipe
        fields = ['title', 'tag', 'cooking_time', 'text', 'picture']
        widgets = {
                   'text': forms.Textarea(attrs={'rows': 8}),
                   }
