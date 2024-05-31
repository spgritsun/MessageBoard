from django import get_version
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.views import image_verify, NoImageException, handle_uploaded_file

if get_version() >= "4.0":
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _
from main.forms import PostForm
from main.models import Post, Comment, Category, Author


# Create your views here.
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


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_post'
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'main/post_create.html'

    def form_valid(self, form):
        form.instance.author = Author.objects.get(user_id=self.request.user.pk)  # Устанавливаем текущего пользователя
        # как
        # автора поста
        return super().form_valid(form)


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному посту.
    model = Post
    # Используем другой шаблон — post_detailed.html
    template_name = 'main/post_detailed.html'
    # Название объекта, в котором будет выбранная новость
    context_object_name = 'post'
    queryset = Post.objects.all()


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_post'
    form_class = PostForm
    model = Post
    template_name = 'main/post_edit.html'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'main.delete_post'
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
def upgrade_me(request):
    user = request.user
    Author.objects.create(user=user)
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/login/')


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    subscriber = True

    message = 'Вы успешно подписались на рассылку постов категории'
    return render(request, 'main/subscribe.html', {'category': category, 'message': message, 'subscriber': subscriber})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if user in category.subscribers.all():
        category.subscribers.remove(user)
        subscriber = False
        message = 'Вы успешно отписались от рассылки постов категории'
        return render(request, 'main/subscribe.html',
                      {'category': category, 'message': message, 'subscriber': subscriber})


@login_required
def upload_file(request):
    if request.method == "POST" and request.user.is_active:
        form = UploadFileForm(request.POST, request.FILES)
        allow_all_file_types = getattr(settings, "CKEDITOR_5_ALLOW_ALL_FILE_TYPES", False)

        if not allow_all_file_types:
            try:
                image_verify(request.FILES['upload'])
            except NoImageException as ex:
                return JsonResponse({"error": {"message": f"{ex}"}}, status=400)
        if form.is_valid():
            url = handle_uploaded_file(request.FILES["upload"])
            return JsonResponse({"url": url})
    raise Http404(_("Page not found."))
