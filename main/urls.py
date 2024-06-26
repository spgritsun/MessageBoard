from django.urls import path
from main.views import*

urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('posts/', PostList.as_view(), name='post_list'),
    path('current-user-posts/', CurrentUserPostList.as_view(), name='current_user_post_list'),
    path('current-user-comments/', CurrentUserCommentList.as_view(), name='current_user_comment_list'),
    path('current-user-post-comments/', CommentList.as_view(), name='current_user_post_comment_list'),
    path('posts/create/', PostCreate.as_view(), name='post_create'),
    path('comments/create/<int:pk>/', CommentCreate.as_view(), name='comment_create'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),
    path('posts/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('comments/<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),
    path('comments/<int:pk>/accept/', comment_accept, name='comment_accept'),
    path('categories/<int:pk>', CategoryPostListView.as_view(), name='category_post_list'),
    path('author/<int:pk>', AuthorPostListView.as_view(), name='author_post_list'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    path('commentators/<int:pk>', CommentListByUser.as_view(), name='commentators'),


]
