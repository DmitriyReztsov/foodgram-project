from django.contrib.auth import get_user_model
from django import template

from recepies.models import Ingredient, Follow, Favorite, ShopingList, Recipe

User = get_user_model()

register = template.Library()


@register.filter()
def filter_favorities(recipe, user):
    return user.favorites.filter(recipe=recipe).exists()


@register.filter()
def filter_purchases(recipe, user):
    return user.shoping.filter(recipe=recipe).exists()
