from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recepies.models import Favorite, Follow, Ingredient, Recipe, ShopingList

from .serializers import IngredientSerializer

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
                        author=get_object_or_404(User, id=author_id)
                        )
        return Response({"success": True}, status=status.HTTP_201_CREATED)
    return Response({"success": False}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['DELETE'])
def remove_subscription(request, id):
    if request.user.id != id:
        unfollow = get_object_or_404(
                    Follow,
                    user=request.user,
                    author=get_object_or_404(User, id=id)
                    )
        unfollow.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
    return Response({"success": False}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def add_favorities(request):
    recipe_id = request.data.get('id')
    new_follow = Favorite.objects.get_or_create(
                    user=request.user,
                    recipe=get_object_or_404(Recipe, id=recipe_id)
                    )
    return Response({"success": True}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def remove_favorities(request, id):
    unfollow = get_object_or_404(
                    Favorite,
                    user=request.user,
                    recipe=get_object_or_404(Recipe, id=id)
                    )
    unfollow.delete()
    return Response({"success": True}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_purchases(request):
    recipe_id = request.data.get('id')
    new_purchase = ShopingList.objects.get_or_create(
                        user=request.user,
                        recipe=get_object_or_404(Recipe, id=recipe_id)
                        )
    return Response({"success": True}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def remove_purchases(request, id):
    del_purchase = get_object_or_404(
                        ShopingList,
                        user=request.user,
                        recipe=get_object_or_404(Recipe, id=id)
                        )
    del_purchase.delete()
    return Response({"success": True}, status=status.HTTP_200_OK)
