from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.reports, name='reports'),
    path('reports/cursos_mas_ausencias/', views.report_cursos_mas_ausencias, name='report_cursos_mas_ausencias'),
    path('reports/download_pdf_report/', views.download_pdf_report, name='download_pdf_report'),
    path('reports/latePayments/', views.latePayments, name='latePayments'),
    path('reports/coursesRanking', views.coursesRanking, name='coursesRanking'),
    path('reports/revenues', views.revenues, name='revenues'),
    path('reports/get_revenues_per_year/<int:year>', views.get_revenues_per_year, name='get_revenues_per_year')
]