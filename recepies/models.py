from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    unit = models.CharField(max_length=10)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title}, {self.unit}"


class Tag(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=CASCADE)
    title = models.CharField(max_length=200, verbose_name="Название рецепта")
    picture = models.ImageField(upload_to='recepies/', blank=True, null=True,
                                verbose_name="Загрузить фото",
                                help_text="Find and attach your file")
    text = models.TextField(verbose_name="Описание",
                            help_text="Type your recipe here")
    ingredients = models.ManyToManyField(Ingredient,
                                         through="QuantityIngreds",
                                         verbose_name="Ингредиенты")
    tag = models.ManyToManyField(Tag, verbose_name="Теги",
                                 help_text="Choose tags",
                                 blank=True, null=True)
    cooking_time = models.PositiveIntegerField(
                        verbose_name="Время приготовления",
                        help_text="Insert cooking time"
                        )
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class QuantityIngreds(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE,
                               related_name='quantityingred')
    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE,
                                   related_name='quantityingred')
    quantity = models.PositiveIntegerField()


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=CASCADE,
                               related_name="following")


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE,
                               related_name='favorites')

    class Meta:
        ''' Ограничение: пара пользователь-рецепт должна быть уникальна
        и не повторяться.

        '''
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe'
            )
        ]


class ShopingList(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='shoping')
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE,
                               related_name='shoping')
