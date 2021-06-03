from django import forms

from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    OPTIONS = (
                ("brfst", "Завтрак"),
                ("lnch", "Обед"),
                ("dnr", "Ужин"),
                )
    tags = forms.MultipleChoiceField(
                choices=OPTIONS,
                label='ТЕГИ',
                required=False,
                widget=forms.CheckboxSelectMultiple(
                    attrs={'class': 'tags__checkbox'}
                    )
                )

    def clean(self):
        cleaned_data = super(RecipeForm, self).clean()
        if cleaned_data.get("tags"):
            self.tag = Tag.objects.filter(slug__in=cleaned_data.get("tags"))
        return cleaned_data

    class Meta:
        model = Recipe
        fields = ['title', 'tag', 'cooking_time', 'text', 'picture']
        widgets = {
                   'text': forms.Textarea(attrs={'rows': 8}),
                   }
