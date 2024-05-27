from django.urls import path

from main import views
from main.views import PostList, PostCreate

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/create/', PostCreate.as_view(), name='post_create'),
]