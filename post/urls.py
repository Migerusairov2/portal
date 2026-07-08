from django.urls import path
from . import views

urlpatterns = [
    path("post/", views.post_list, name="post_list"),
    path("post/new/", views.add_post, name="add_post"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
]