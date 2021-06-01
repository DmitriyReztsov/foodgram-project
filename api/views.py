from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import IngredientSerializer
from rest_framework import status

from recepies.models import Ingredient, Follow, Favorite, ShopingList, Recipe

User = get_user_model()


@api_view(['GET'])
def get_ingredients(request):
    letters = request.GET.get('query', '')
    qs = Ingredient.objects.filter(title__istartswith=letters)
    serializer = IngredientSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_subscription(request):
    author_id = request.data.get('id')
    if request.user.id != author_id:
        new_follow = Follow.objects.get_or_create(
                        user=request.user,
                        author=User.objects.get(id=author_id)
                        )
        return Response({"success": True}, status=status.HTTP_201_CREATED)
    return Response({"success": False}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['DELETE'])
def remove_subscription(request, id):
    if request.user.id != id:
        unfollow = Follow.objects.get(
                    user=request.user,
                    author=User.objects.get(id=id)
                    )
        unfollow.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
    return Response({"success": False}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def add_favorities(request):
    recipe_id = request.data.get('id')
    new_follow = Favorite.objects.get_or_create(
                    user=request.user,
                    recipe=Recipe.objects.get(id=recipe_id)
                    )
    return Response({"success": True}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def remove_favorities(request, id):
    unfollow = Favorite.objects.get(
                    user=request.user,
                    recipe=Recipe.objects.get(id=id)
                    )
    unfollow.delete()
    return Response({"success": True}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_purchases(request):
    recipe_id = request.data.get('id')
    new_purchase = ShopingList.objects.get_or_create(
                        user=request.user,
                        recipe=Recipe.objects.get(id=recipe_id)
                        )
    return Response({"success": True}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def remove_purchases(request, id):
    del_purchase = ShopingList.objects.get(
                        user=request.user,
                        recipe=Recipe.objects.get(id=id)
                        )
    del_purchase.delete()
    return Response({"success": True}, status=status.HTTP_200_OK)
