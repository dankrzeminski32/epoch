from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from register import views as v
from register.forms import CustomAuthForm
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/',
         auth_views.LoginView.as_view(authentication_form=CustomAuthForm), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(), name="logout"),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('accounts/register/', v.register, name="register")
]
