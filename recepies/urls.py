from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("create/", views.create_recipe, name="create"),
    path("follow/", views.follow_index, name="follow_index"),
    path("favorities/", views.Favorities.as_view(), name="favorities"),
    path("profile/<str:username>/", views.UserProfile.as_view(),
         name="profile"),
    path("recepies/<int:pk>/", views.SinglePost.as_view(), name="post"),
    path("<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("<int:post_id>/delete/", views.post_delete, name="post_delete"),
    path("<str:username>/follow/", views.profile_follow, name="my_subscribes"),
    path("<str:username>/unfollow/", views.profile_unfollow,
         name="profile_unfollow"),
    path("shopinglist/", views.ShopingListView.as_view(), name="shoping_list"),
    path("shopinglist/download/", views.shoping_list_download,
         name="shoping_list_download"),
    ]
