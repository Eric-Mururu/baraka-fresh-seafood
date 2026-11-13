from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import CustomerAuthenticationForm

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('account/register/', views.register, name='register'),
    path(
        'account/login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=CustomerAuthenticationForm,
        ),
        name='login',
    ),
    path('account/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('account/', views.account, name='account'),
]