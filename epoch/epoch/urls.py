from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from register import views as v
from register.forms import CustomAuthForm
from django.contrib.auth import views as auth_views
from . import views as general_views
import sources


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/',
         auth_views.LoginView.as_view(authentication_form=CustomAuthForm), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(), name="logout"),
    path("", general_views.home, name="home"),
    path('accounts/register/', v.register, name="register"),
    path("sources/", include("sources.urls")),
    path("news/", sources.views.news, name="news"),
    path("news/detail/<int:headline_id>",
         sources.views.news_detail, name="news-detail")
]
