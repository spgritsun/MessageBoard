from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(verbose_name='Название категории', max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories', blank=True, verbose_name='Подписчики')

    def __str__(self):
        return self.category_name


class Post(models.Model):
    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='Время создания поста', default=timezone.now)
    categories = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категории')
    title = models.CharField(max_length=200, verbose_name='Заголовок поста')
    text = CKEditor5Field(config_name='extends', verbose_name='Текст поста')

    def get_absolute_url(self):
        return reverse('post_list')  # , args=[str(self.id)]

    def __str__(self):
        return f' {self.time}, {self.title}, {self.text[:30]}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='ID поста')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ID комментария')
    comment_text = models.TextField(max_length=500, verbose_name='Текст комментария')
    comment_time = models.DateTimeField(default=timezone.now, verbose_name='Время создания комментария')
    is_accepted = models.BooleanField(default=False, verbose_name='Комментарий принят')

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.comment_text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title}, {self.post.time}, {self.category.category_name}'
