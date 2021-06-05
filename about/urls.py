from django.urls import path

from . import views

urlpatterns = [
    path("about_me/", views.AboutMePage.as_view(), name="about_me"),
    path("technologies/", views.AboutTechPage.as_view(), name="technologies"),
]
