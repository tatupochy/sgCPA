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
from django.urls import path
from accounts.views import CustomLoginView, CustomSignupView, ListUsersView, UserDetailView, UserEditView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/signup/', CustomSignupView.as_view(), name='signup'),
    path('accounts/users/', ListUsersView.as_view(), name='users'),
    path('accounts/users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('accounts/users/<int:pk>/edit/', UserEditView.as_view(), name='user_edit'),
]
