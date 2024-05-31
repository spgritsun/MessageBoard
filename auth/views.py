from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from main.models import Author


class PersonalView(LoginRequiredMixin, TemplateView):
    template_name = 'auth/personal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['in_group_author'] = self.request.user.groups.filter(name='authors').exists()
        context['in_model_author'] = Author.objects.filter(user_id=self.request.user.pk).exists()
        return context
