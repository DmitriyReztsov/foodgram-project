from django.contrib import admin
from django.db.models import Count

from .models import (Favorite, Follow, Ingredient, QuantityIngreds, Recipe,
                     ShopingList, Tag)


class QuantityIngredsInline(admin.TabularInline):
    model = QuantityIngreds
    extra = 1
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (QuantityIngredsInline,)
    list_display = ('title', 'author', 'total_favors',)
    list_filter = ('author', 'title', 'tag',)
    readonly_fields = ('total_favors',)
    autocomplete_fields = ['ingredients']

    def total_favors(self, instance):
        result = Favorite.objects.filter(
                    recipe=instance
                    ).aggregate(
                        Count("user")
                        )
        return result["user__count"]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit')
    list_filter = ('title',)
    search_fields = ['title']


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(QuantityIngreds)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(ShopingList)
