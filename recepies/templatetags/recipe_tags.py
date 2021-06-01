from django import template
from django.contrib.auth import get_user_model
from urllib.parse import urlencode

from recepies.models import Ingredient, Follow, Favorite, Recipe
from recepies.models import Tag, ShopingList

User = get_user_model()

register = template.Library()


@register.simple_tag()
def get_tags(filter=None):
    print(filter)
    return Tag.objects.all()


@register.simple_tag()
def add_tag(request, tag):
    """В словаре request.GET содержится список tag из адресной строки
    текущей страницы.
    Если там уже содержится тег, для которого собирается ссылка, - удаляем,
    иначе - добавляем в список. Из полученного списка формируем часть
    параметров запроса ссылки.

    """
    current_tags = request.GET.getlist('tag')
    if tag.slug in current_tags:
        current_tags.remove(tag.slug)
    else:
        current_tags.append(tag.slug)
    return urlencode({'tag': current_tags}, doseq=True)


@register.simple_tag()
def activate_tag(request, tag):
    """Если в словаре есть тег - передаем часть css-класса, которая
    показывает тег активным.

    """
    current_tags = request.GET.getlist('tag')
    if tag.slug in current_tags:
        return 'tags__checkbox_active'


@register.simple_tag()
def filter_tag(request):
    """Для перехода по страницам надо добавить текущий поисковый запрос
    к номеру страницы паджинатора.

    """
    current_tags = request.GET.getlist('tag')
    if current_tags:
        return f'&{urlencode({"tag": current_tags}, doseq=True)}'
    return ""


@register.simple_tag()
def purchase_counter(request):
    print(request)
    return ShopingList.objects.filter(user=request.user).count()
