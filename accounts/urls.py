from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import (
    CustomUserCreationForm,
    CustomPasswordResetForm,
    CustomPasswordResetConfirmForm
)

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),

    # 密码重置流程
    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name='accounts/password_reset_form.html',
            email_template_name='accounts/password_reset_email.html',
            success_url='sent/'
        ),
        name='password_reset'
    ),
    path(
        'reset-password/sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            form_class=CustomPasswordResetConfirmForm,
            success_url='/accounts/login/'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]