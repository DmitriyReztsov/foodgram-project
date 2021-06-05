from recepies.models import ShopingList


def purchases_count(request):
    if request.user.is_authenticated:
        count = ShopingList.objects.filter(user=request.user).count()
    else:
        count = 0
    return {
        "purchases_count": count
    }
