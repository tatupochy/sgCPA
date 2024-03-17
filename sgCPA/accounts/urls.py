from django.urls import path
from . import views
from .views import CustomLoginView, users_view, user_detail_view, user_edit_view, user_create_view, user_delete_view

urlpatterns = [
    path('accounts/login', CustomLoginView.as_view(), name='login'),
    path('accounts/users/', users_view, name='users'),
    path('accounts/users/create/', user_create_view, name='user_create'),
    path('accounts/users/<int:pk>/', user_detail_view, name='user_detail'),
    path('accounts/users/<int:pk>/edit/', user_edit_view, name='user_edit'),
    path('accounts/users/<int:pk>/delete/', views.user_delete_view, name='user_delete')
]