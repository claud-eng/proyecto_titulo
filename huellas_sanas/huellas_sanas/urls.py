"""
URL configuration for huellas_sanas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views 
from apps.Usuario.forms import ResetPasswordForm, NewPasswordForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: render(request, 'home.html'), name='home'),
    path('usuario/', include('apps.Usuario.urls')),
    path('cita/', include('apps.Cita.urls')),
    path('cuidado/', include('apps.Cuidado.urls')),
    path('transaccion/', include('apps.Transaccion.urls')),
    path('enviar_consulta/', views.enviar_consulta, name='enviar_consulta'),
    path('consulta_exitosa/', views.consulta_exitosa, name='consulta_exitosa'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('preguntas_frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),
    path('login/', auth_views.LoginView.as_view(template_name='Usuario/login.html'), name='login'),
 # Login and Logout
    path('login/', LoginView.as_view(redirect_authenticated_user=True,template_name='Usuario/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='Usuario/logout.html'), name='logout'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="Usuario/reset_password.html", form_class=ResetPasswordForm), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="Usuario/reset_password_done.html"), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Usuario/reset_password_confirm.html", form_class=NewPasswordForm), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="Usuario/reset_password_complete.html"), name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)