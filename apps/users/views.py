from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegistrationForm
from .models import CreatedSite, PageTransitionStatistic


class IndexView(TemplateView):
    template_name = 'index.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_created_sites'] = CreatedSite.objects.filter(user=self.request.user)
        context['page_transition_statistics'] = PageTransitionStatistic.objects.filter(site__user=self.request.user)
        return context


class RegistrationView(CreateView):
    template_name = 'auth/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('dashboard')


class UserLoginView(LoginView):
    template_name = 'auth/login.html'
