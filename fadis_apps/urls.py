"""fadis_apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django_registration.backends.activation import views as exten_auth_views
from django.urls import path, include
from UAM import views as uam_views
from UAM.forms import UserRegisterForm, ChangePasswordForm, UserLoginForm, ResetPasswordForm, SetNewPasswordForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', exten_auth_views.RegistrationView.as_view(form_class=UserRegisterForm, template_name='UAM/register.html', email_subject_template='UAM/activation_email_subject.txt', email_body_template='UAM/activation_email_body.txt'), name='django_registration_register'),
    path('activate/complete/', TemplateView.as_view(template_name='UAM/activation_complete.html'), name='django_registration_activation_complete'),
    path('activate/<str:activation_key>/', exten_auth_views.ActivationView.as_view(template_name='UAM/activation_failed.html'), name='django_registration_activate'),
    path('register/complete/', TemplateView.as_view(template_name='UAM/registration_complete.html'), name='django_registration_complete'),
    path('register/closed/', TemplateView.as_view(template_name='UAM/registration_closed.html'), name='django_registration_disallowed'),
    path('profile/', login_required(uam_views.profile), name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='UAM/login.html', authentication_form=UserLoginForm, redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='UAM/logout.html'), name='logout'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='UAM/password_change_done.html'), name='password_change_done'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='UAM/password_change.html', form_class=ChangePasswordForm), name='password_change'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='UAM/password_reset.html', form_class=ResetPasswordForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='UAM/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='UAM/password_reset_confirm.html', form_class=SetNewPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='UAM/password_reset_complete.html'), name='password_reset_complete'),
    path('', include('attendance_tracker.urls')),
]
