from django.urls import path
from . import views
from .views import (CustomLoginView, users_view, user_detail_view, user_edit_view, user_create_view, 
                    user_delete_view, person_create_view, person_detail_view, persons_view, person_edit_view)

urlpatterns = [
    path('accounts/login', CustomLoginView.as_view(), name='login'),
    path('accounts/users/', users_view, name='users'),
    path('accounts/users/create/', user_create_view, name='user_create'),
    path('accounts/users/<int:pk>/', user_detail_view, name='user_detail'),
    path('accounts/users/<int:pk>/edit/', user_edit_view, name='user_edit'),
    path('accounts/users/<int:pk>/delete/', user_delete_view, name='user_delete'),
    path('accounts/persons/', persons_view, name='persons'),
    path('accounts/persons/create/', person_create_view, name='person_create'),
    path('accounts/persons/<int:pk>/', person_detail_view, name='person_detail'),
    path('accounts/persons/<int:pk>/edit/', person_edit_view, name='person_edit'),
]