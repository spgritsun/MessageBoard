from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from main.forms import PostForm
from main.models import Post, Comment, Category


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


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному посту.
    model = Post
    # Используем другой шаблон — post_detailed.html
    template_name = 'main/post_detailed.html'
    # Название объекта, в котором будет выбранная новость
    context_object_name = 'post'
    queryset = Post.objects.all()


class PostUpdate(LoginRequiredMixin, UpdateView):
    # permission_required = 'main.change_post'
    form_class = PostForm
    model = Post
    template_name = 'main/post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'main/post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryPostListView(ListView):
    model = Post
    template_name = 'main/category_post_list.html'
    context_object_name = 'cat_post_context'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('-time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку постов категории'
    return render(request, 'main/subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if user in category.subscribers.all():
        category.subscribers.remove(user)
        message = 'Вы успешно отписались от рассылки постов категории'
        return render(request, 'main/subscribe.html', {'category': category, 'message': message})
