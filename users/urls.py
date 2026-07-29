from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, custom_logout, dashboard_redirect


urlpatterns = [
    path('register/', register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='users/login.html'
        ),
        name='login'
    ),

    path('logout/', custom_logout, name='logout'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
]