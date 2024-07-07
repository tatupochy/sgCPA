from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.reports, name='reports'),
    path('latePayments/', views.latePayments, name='latePayments'),
    path('coursesRanking', views.coursesRanking, name='coursesRanking')
]