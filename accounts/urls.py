from django.contrib.auth.views import LoginView
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView
)
from django.urls import path

from . import views
from .forms import UserPasswordReset, UserPasswordResetConfirm, UserChangePassword

urlpatterns = [
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('profile/view/', views.UserProfileView.as_view(), name='profile'),
    path('address/view/', views.AddressView.as_view(), name='address'),
    path('orders/view/', views.OrdersView.as_view(), name='orders'),
    path('orders/view/<int:pk>/', views.OrderItemView.as_view(), name='order_item'),
    path('address/<int:pk>/update/', views.UpdateAddress.as_view(), name='update_address'),
    path('address/<int:pk>/default/', views.make_default, name='make_default'),
    path('address/<int:pk>/delete/', views.delete_address, name='delete_address'),
    path('reply/admin/', views.AdminReplyView.as_view(), name='admin_reply'),

    #   user authentication urls
    path('', views.UserRegisterView.as_view(), name='register'),
    path('sign-in/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('sign-out/', views.UserLogout.as_view(), name='logout'),

    #   password reset urls
    path('password/reset/',
         PasswordResetView.as_view(template_name="accounts/reset_password.html",
                                   form_class=UserPasswordReset),
         name="password_reset"),

    path('password/reset/done/',
         PasswordResetDoneView.as_view(template_name="accounts/reset_password_done.html"),
         name="password_reset_done"),

    path('password/reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="accounts/reset_password_confirm.html",
                                          form_class=UserPasswordResetConfirm),
         name="password_reset_confirm"),

    path('password/reset/complete/',
         PasswordResetCompleteView.as_view(template_name="accounts/reset_password_complete.html"),
         name="password_reset_complete"),

    #   password change url
    path('password/change/', PasswordChangeView.as_view(
                            template_name="accounts/change_password.html",
                            form_class=UserChangePassword),
                            name="change_password")
]
