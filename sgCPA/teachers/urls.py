from django.urls import path
from teachers import views

urlpatterns = [
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('edit_teachers/<int:pk>', views.teacher_update, name='teacher_update'),
    path('delete_teachers/<int:pk>', views.teacher_delete, name='teacher_delete'),
]
