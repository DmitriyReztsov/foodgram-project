from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http.response import HttpResponse

from .models import Recipe, ShopingList


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
