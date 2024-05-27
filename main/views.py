from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, CreateView

from main.forms import PostForm
from main.models import Post, Comment


# Create your views here.
def index(request):
    return HttpResponse("Привет, мир! Это мой первый веб-сайт на Django.")


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'main/posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10


class PostCreate(CreateView):  # PermissionRequiredMixin,
    # permission_required = 'main.add_post'
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'main/post_create.html'
