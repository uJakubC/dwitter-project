"""Dwitter_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from Dwitter.class_views import MainPageView
from Users.class_views import LogoutView, LoginView, RegisterView

urlpatterns = [
    path('', MainPageView.as_view(), name='main-page'),
    path('admin/', admin.site.urls),

    # User auth views
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Dwitter app views
    path('dwitter/', include('Dwitter.urls')),
    # Users app views
    path('users/', include('Users.urls'))
]
