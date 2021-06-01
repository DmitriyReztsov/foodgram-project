from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum

from .models import Recipe, Ingredient, Tag, QuantityIngreds, Follow, Favorite
from .models import ShopingList
from .forms import RecipeForm

User = get_user_model()


class Index(ListView):
    model = Recipe
    template_name = 'index.html'
    # переопределяем стандартную коллекцию object_list
    context_object_name = 'page'
    paginate_by = 9
    title = 'Рецепты'

    ''' Определяем queryset для фильтрации.

    '''
    def get_queryset(self):
        qs = self.request.GET.getlist('tag')
        if qs:
            return Recipe.objects.filter(tag__slug__in=qs)
        return Recipe.objects.all()

    ''' Переопределяем метод get_context_data, потдверждая родительский метод и
    добавляя в словарь context допольнительную информацию.

    '''
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['tags'] = Tag.objects.all()
        return context


class UserProfile(ListView):
    model = Recipe
    template_name = 'authorRecipe.html'
    context_object_name = 'page'
    paginate_by = 9

    def get_queryset(self):
        qs = self.request.GET.getlist('tag')
        if qs:
            return Recipe.objects.filter(
                        author__username=self.kwargs['username'],
                        tag__slug__in=qs
                        )
        return Recipe.objects.filter(author__username=self.kwargs['username'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Страница пользователя {self.kwargs['username']}"
        context['tags'] = Tag.objects.all()
        context['profile_user'] = get_object_or_404(
                                    User,
                                    username=self.kwargs['username']
                                    )
        if self.request.user in Follow.objects.filter(
                                    author__username=self.kwargs['username']
                                    ):
            context['follow'] = True
        else:
            context['follow'] = False
        return context


class SinglePost(DetailView):
    model = Recipe
    template_name = 'singlePage.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рецепт'
        context['ingreds'] = QuantityIngreds.objects.filter(
                                recipe_id=self.kwargs['pk']
                                )
        context['tags'] = Tag.objects.filter(recipe=self.kwargs['pk'])
        return context


def create_entry(new_entry, request_dict):
    ingred_list = []
    for item in request_dict.items():
        print(item)
        if item[0] == 'breakfast':
            tag = get_object_or_404(Tag, slug='brfst')
            new_entry.tag.add(tag)
        if item[0] == 'lunch':
            tag = get_object_or_404(Tag, slug='lnch')
            new_entry.tag.add(tag)
        if item[0] == 'dinner':
            tag = get_object_or_404(Tag, slug='dnr')
            new_entry.tag.add(tag)
        if item[0].startswith('nameIngredient'):
            name_ingred = item[1]
        if item[0].startswith('valueIngredient'):
            value_ingred = item[1]
        if item[0].startswith('unitsIngredient'):
            units_ingred = item[1]
            ingredient = get_object_or_404(
                            Ingredient,
                            title=name_ingred,
                            unit=units_ingred
                            )
            ingred_list.append(QuantityIngreds(
                                    recipe=new_entry,
                                    ingredient=ingredient,
                                    quantity=value_ingred
                                    )
                               )
    QuantityIngreds.objects.bulk_create(ingred_list)


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        with transaction.atomic():
            new_entry = form.save(commit=False)
            new_entry.author = request.user
            new_entry.author = request.user
            new_entry.save()
            create_entry(new_entry, request.POST)
        return redirect('index')

    return render(
                request,
                "formRecipe.html",
                {
                    'form': form,
                    'title': 'Создание рецепта'
                }
                )


@login_required
def post_edit(request, post_id):
    recipe = get_object_or_404(Recipe, id=post_id)
    ingreds = QuantityIngreds.objects.filter(recipe=recipe)
    tags = Tag.objects.filter(recipe__id=recipe.id)
    tags_slug_list = []
    for tag in tags:
        tags_slug_list.append(tag.slug)
    if request.user != recipe.author:
        return redirect('post', id=post_id)

    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)

    if form.is_valid():
        with transaction.atomic():
            new_entry = form.save(commit=False)
            new_entry.author = request.user
            new_entry.author = request.user
            new_entry.save()
            for obj in ingreds:
                obj.delete()
            for tag in tags:
                '''удаляет связь между объектом рецепта (recipe)
                по полю m2m (tag) для объекта tag(2)

                '''
                recipe.tag.remove(tag)
            create_entry(new_entry, request.POST)
        return redirect('index')
    print(form.instance.id)
    return render(
                request,
                "formRecipe.html",
                {
                    'form': form,
                    'ingredients': ingreds,
                    'tags': tags_slug_list,
                    'title': 'Редактирование рецепта',
                    'edit': True
                }
            )


@login_required
def post_delete(request, post_id):
    recipe = get_object_or_404(Recipe, id=post_id)
    if request.user != recipe.author:
        return redirect('post', pk=post_id)
    recipe.delete()
    return redirect('index')


@login_required
def follow_index(request):
    authors_list = Follow.objects.filter(user=request.user)
    paginator = Paginator(authors_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    title = f'{"Мои подписки"}'
    return render(request, "myFollow.html",
                  {'title': title,
                   'page_obj': page,
                   'paginator': paginator}
                  )


@login_required
def profile_follow(request, username):
    if request.user.username != username:
        new_follow = Follow.objects.get_or_create(
                        user=request.user,
                        author=User.objects.get(username=username))
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    un_follow = Follow.objects.get(user=request.user, author=author)
    un_follow.delete()
    return redirect('profile', username=username)


class Favorities(ListView):
    model = Recipe
    template_name = 'favorities.html'
    context_object_name = 'page'
    paginate_by = 9
    title = 'Избранное'

    ''' Определяем queryset для фильтрации.

    '''
    def get_queryset(self):
        qs = self.request.GET.getlist('tag')
        if qs:
            return Recipe.objects.filter(
                    favorites__in=Favorite.objects.filter(
                        user=self.request.user
                        ),
                    tag__slug__in=qs)
        return Recipe.objects.filter(
                favorites__in=Favorite.objects.filter(
                    user=self.request.user
                    )
                )

    ''' Переопределяем метод get_context_data, потдверждая родительский метод и
    добавляя в словарь context допольнительную информацию.

    '''
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['tags'] = Tag.objects.all()
        return context


class ShopingListView(ListView):
    model = Recipe
    template_name = 'shopList.html'
    context_object_name = 'page'
    paginate_by = 9
    title = 'Список покупок'

    def get_queryset(self):
        return Recipe.objects.filter(
                shoping__in=ShopingList.objects.filter(
                    user=self.request.user
                    )
                )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


@login_required
def shoping_list_download(request):
    list_recipes = Recipe.objects.filter(
        shoping__in=ShopingList.objects.filter(user=request.user)
        )
    ingredients = list_recipes.order_by('ingredients__title').values(
                'ingredients__title',
                'ingredients__unit').annotate(
                total_quantity=Sum('quantityingred__quantity'))
    content = ''
    for ingredient in ingredients:
        print(ingredient)
        content += (f'{ingredient["ingredients__title"]}'
                    f' - {ingredient["total_quantity"]}'
                    f' {ingredient["ingredients__unit"]}\n')
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
                                        'shopping_list.txt'
                                        )
    return response
