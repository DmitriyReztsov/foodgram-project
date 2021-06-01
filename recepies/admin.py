from django.contrib import admin
from django.db.models import Count

from .models import Ingredient, Tag, Recipe, QuantityIngreds, Follow, Favorite
from .models import ShopingList


class MembershipInline(admin.TabularInline):
    model = QuantityIngreds
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)
    list_display = ('title', 'author', 'total_favors',)
    list_filter = ('author', 'title', 'tag',)
    readonly_fields = ('total_favors',)

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


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(QuantityIngreds)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(ShopingList)
