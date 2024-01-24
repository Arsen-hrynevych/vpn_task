from django.urls import path
from .views import (
    IndexView,
    UserLoginView,
    RegistrationView,
    DashboardView,
)
from .utils import (
    edit_profile,
    create_site,
    internal_redirect
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('create_site/', create_site, name='create_site'),
    path('<str:user_site_name>/<path:routes>/', internal_redirect, name='internal_redirect')
]

