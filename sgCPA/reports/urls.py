from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.reports, name='reports'),
    path('reports/cursos_mas_ausencias/', views.report_cursos_mas_ausencias, name='report_cursos_mas_ausencias'),
    # path('reports/download_pdf_report/', views.download_pdf_report, name='download_pdf_report'),
    path('reports/latePayments/', views.latePayments, name='latePayments'),
    path('reports/latePayments/<int:year>/<int:month>/', views.latePayments, name='latePayments_month_year'),
    path('reports/coursesRanking', views.coursesRanking, name='coursesRanking'),
    path('reports/get_courses_ranking_filter/<int:year>/', views.get_courses_ranking_filter, name='courses_ranking_year_filter'),
    path('reports/get_courses_ranking_filter/<int:year>/<int:month>', views.get_courses_ranking_filter, name='courses_ranking__month_year_filter'),
    path('reports/get_courses_ranking_filter/<int:year>/<int:month>/<int:shift_id>', views.get_courses_ranking_filter, name='courses_ranking__month_year_shift_filter'),
    path('reports/revenues', views.revenues, name='revenues'),
    path('reports/get_revenues_per_year/<int:year>', views.get_revenues_per_year, name='get_revenues_per_year'),
    path('reports/get_revenues_per_year/<int:year>/<int:month>', views.get_revenues_per_year, name='get_revenues_per_year_month'),
    path('reporte_matriculas/', views.reporte_matriculas, name='reporte_matriculas'),
    path('reports/download_pdf_report_matriculados_anho/', views.download_pdf_report_matriculados_anho, name='download_pdf_report_matriculados_anho'),
]