from django.urls import path

from .views import get_ingredients, add_subscription, remove_subscription
from .views import add_favorities, remove_favorities, add_purchases
from .views import remove_purchases

urlpatterns = [
    path('ingredients/', get_ingredients),
    path('subscriptions/', add_subscription),
    path('subscriptions/<int:id>/', remove_subscription),
    path('favorites/', add_favorities),
    path('favorites/<int:id>/', remove_favorities),
    path('purchases/', add_purchases),
    path('purchases/<int:id>/', remove_purchases),
]
