from django.urls import path

from main import views
from main.views import PostList, PostCreate, PostDetail, PostUpdate, PostDelete, subscribe, unsubscribe

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/create/', PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]