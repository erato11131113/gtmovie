from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 原有路由
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),

    # 以下为密码重置相关路由

    # 1. 用户输入邮箱的页面
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset_form.html'
        ),
        name='password_reset'
    ),

    # 2. 提交邮箱成功后提示的页面
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # 3. 用户点邮件链接进入设置新密码的页面 (带 uidb64 和 token 的路由)
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # 4. 设置新密码完成后的提示页面
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
