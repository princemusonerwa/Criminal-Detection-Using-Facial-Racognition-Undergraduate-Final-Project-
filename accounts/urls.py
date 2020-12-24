from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('user/create', views.register, name="register"),
    path('user', views.allUsers, name="users"),
    path('profile', views.profile, name="profile"),
    path('login', auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout', auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
]