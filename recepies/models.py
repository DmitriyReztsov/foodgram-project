from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name="Ингредиент")
    unit = models.CharField(max_length=10,
                            verbose_name="Единица измерения")

    class Meta:
        ordering = ['title']
        verbose_name = "Объект ингредиента'"
        verbose_name_plural = "Объекты ингредиентов"

    def __str__(self):
        return f"{self.title}, {self.unit}"


class Tag(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name="Тег")
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True,
                            verbose_name="Слаг")

    class Meta:
        verbose_name = "Объект тега'"
        verbose_name_plural = "Объекты тегов"

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=CASCADE,
                               verbose_name="Автор рецепта")
    title = models.CharField(max_length=200, verbose_name="Название рецепта")
    picture = models.ImageField(upload_to='recepies/', blank=True, null=True,
                                verbose_name="Загрузить фото",
                                help_text="Загрузите файл с картинкой")
    text = models.TextField(verbose_name="Описание рецепта",
                            help_text="Напишите здесь свой рецепт")
    ingredients = models.ManyToManyField(Ingredient,
                                         blank=False,
                                         through="QuantityIngreds",
                                         verbose_name="Ингредиенты")
    tag = models.ManyToManyField(Tag, verbose_name="Теги",
                                 help_text="Choose tags",
                                 blank=True)
    cooking_time = models.PositiveIntegerField(
                        validators=[MinValueValidator(1)],
                        verbose_name="Время приготовления",
                        help_text="Insert cooking time"
                        )
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Объект рецепта'"
        verbose_name_plural = "Объекты рецептов"

    def __str__(self):
        return self.title


class QuantityIngreds(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE,
                               related_name='quantityingred',
                               verbose_name="Рецепт")
    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE,
                                   related_name='quantityingred',
                                   verbose_name="Ингредиент")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                           verbose_name="Количество")

    class Meta:
        verbose_name = "Объект промежуточной модели ингредиентов'"
        verbose_name_plural = "Объекты промежуточной модели ингредиентов"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="follower",
                             verbose_name="Пользователь")
    author = models.ForeignKey(User, on_delete=CASCADE,
                               related_name="following",
                               verbose_name="Интересный автор")

    class Meta:
        verbose_name = "Объект подписки'"
        verbose_name_plural = "Объекты подписок"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='favorites',
                             verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE,
                               related_name='favorites',
                               verbose_name="Любимый рецепт")

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
        verbose_name = "Объект избранного рецепта'"
        verbose_name_plural = "Объекты избранных рецептов"


class ShopingList(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='shoping',
                             verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE,
                               related_name='shoping',
                               verbose_name="Рецепт купить")

    class Meta:
        verbose_name = "Объект списка покупок'"
        verbose_name_plural = "Объекты списков покупок"
