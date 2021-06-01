from random import choice

import factory
from factory import fuzzy

from users.factories import UserFactory

from . import models


class BaseRecipeFactory(factory.django.DjangoModelFactory):
    """Factory that generates Recipes without Ingredients."""
    author = factory.SubFactory(UserFactory)
    title = factory.Faker('word')
    picture = factory.django.ImageField(width=1000)
    text = factory.Faker('text')
    # no ingredients
    cooking_time = fuzzy.FuzzyInteger(10, 120)

    class Meta:
        model = models.Recipe


class QuantityIngredsFactory(factory.django.DjangoModelFactory):
    """Factory that generates Recipes with Ingredients."""
    recipe = factory.SubFactory(BaseRecipeFactory)
    quantity = fuzzy.FuzzyInteger(50, 500)

    class Meta:
        model = models.QuantityIngreds

    @factory.lazy_attribute
    def ingredient(self):
        return choice(models.Ingredient.objects.all())


class RecipeFactory(BaseRecipeFactory):
    """Factory that generates Recipes with 5 Ingredients."""

    ingredient_1 = factory.RelatedFactory(
        QuantityIngredsFactory,
        factory_related_name='recipe',
    )
    ingredient_2 = factory.RelatedFactory(
        QuantityIngredsFactory,
        factory_related_name='recipe',
    )
    ingredient_3 = factory.RelatedFactory(
        QuantityIngredsFactory,
        factory_related_name='recipe',
    )
    ingredient_4 = factory.RelatedFactory(
        QuantityIngredsFactory,
        factory_related_name='recipe',
    )
    ingredient_5 = factory.RelatedFactory(
        QuantityIngredsFactory,
        factory_related_name='recipe',
    )
