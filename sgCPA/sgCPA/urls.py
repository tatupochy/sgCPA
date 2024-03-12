"""
URL configuration for sgCPA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from accounts.views import CustomLoginView, users_view, user_detail_view, user_edit_view, user_create_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login', CustomLoginView.as_view(), name='login'),
    path('accounts/users/', users_view, name='users'),
    path('accounts/users/create/', user_create_view, name='user_create'),
    path('accounts/users/<int:pk>/', user_detail_view, name='user_detail'),
    path('accounts/users/<int:pk>/edit/', user_edit_view, name='user_edit'),
    path('', include('students.urls')),
]
