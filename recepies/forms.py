from django import forms
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _

from .models import Recipe


class RecipeForm(forms.ModelForm):
    valueIngred = forms.IntegerField(
                    required=False,
                    validators=[MinValueValidator(1)]
                    )

    class Meta:
        model = Recipe
        fields = ['title', 'cooking_time', 'text', 'picture']
        widgets = {
                   'text': forms.Textarea(attrs={'rows': 8}),
                   }
        error_messages = {
            'cooking_time': {
                'min_value': _('Готовим по земному времени'
                               '- не менее 1 минуты'),
            },
        }
