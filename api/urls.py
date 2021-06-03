from django.urls import path

from .views import (add_favorities, add_purchases, add_subscription,
                    get_ingredients, remove_favorities, remove_purchases,
                    remove_subscription)

urlpatterns = [
    path('ingredients/', get_ingredients),
    path('subscriptions/', add_subscription),
    path('subscriptions/<int:id>/', remove_subscription),
    path('favorites/', add_favorities),
    path('favorites/<int:id>/', remove_favorities),
    path('purchases/', add_purchases),
    path('purchases/<int:id>/', remove_purchases),
]
