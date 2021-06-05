from django import forms

from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'cooking_time', 'text', 'picture']
        widgets = {
                   'text': forms.Textarea(attrs={'rows': 8}),
                   }
