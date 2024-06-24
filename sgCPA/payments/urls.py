from django.urls import path
from . import views
from .views import (
    payments,
    payment_detail,
    search_pending_payments,
    payment_invoice_create,
    fees,
    fee_detail,
    fee_create,
    enrollments,
    enrollment_detail,
    enrollment_detail_payment,
    enrollment_create,
    enrollment_edit,
    enrollment_eliminar,
    create_fees,
    payment_method_create,
    payment_method_list,
    concept_create,
    concept_list,
    concept_edit,
    concept_delete,
    concept_detail,
    get_students,
    enrollment_detail_create
)
urlpatterns = [
    path('payments/', payments, name='payments'),
    path('payments/<int:payment_id>/', payment_detail, name='payment_detail'),
    path('payments/search_pending_payments/', search_pending_payments, name='search_pending_payments'),
    path('payments/pending_payments/<int:pk>/', views.pending_payments, name='pending_payments'),
    path('payments/create/invoice/<int:pk>', payment_invoice_create, name='payment_invoice_create'),
    path('show_payment_resume/<int:pk>', views.show_payment_resume, name='show_payment_resume'),
    ########
    path('invoices/', views.invoices, name='invoices'),
    path('show_invoice/<int:pk>', views.show_invoice, name='show_invoice'),
    path('download_invoice/<int:pk>', views.download_invoice, name='download_invoice'),
    ########
    path('fees/', fees, name='fees'),
    path('fees/<int:fee_id>/', fee_detail, name='fee_detail'),
    path('fees/create/', fee_create, name='fee_create'),
    path('fees/create_fees/<int:student_id>', create_fees, name='create_fees'),
    ########
    path('enrollments/', enrollments, name='enrollments'),
    path('enrollments/<int:enrollment_id>/', enrollment_edit, name='enrollment_edit'),
    path('enrollments/details/<int:enrollment_id>/', enrollment_detail, name='enrollment_detail'),
    path('enrollments/<int:enrollment_id>/detail_payment', enrollment_detail_payment, name='enrollment_detail_payment'),
    path('enrollments/create/', enrollment_create, name='enrollment_create'),
    path('enrollments/get_students/<int:courseId>/', views.get_students),
    path('enrollment_eliminar/<int:id>/', views.enrollment_eliminar, name='enrollment_eliminar'),
    path('enrollment_detail_create/<int:enrollment_id>/', enrollment_detail_create, name='enrollment_detail_create'),

    ########
    path('payment_methods/create/', views.payment_method_create, name='payment_method_create'),
    path('payment_methods/', views.payment_method_list, name='payment_method_list'),
    path('edit_payment_methods/<int:payment_method_id>', views.payment_method_edit, name='payment_method_edit'),
    path('delete_payment_methods/<int:payment_method_id>', views.payment_method_delete, name='payment_method_delete'),
    ########
    path('concepts/create/', concept_create, name='concept_create'),
    path('concepts/', concept_list, name='concept_list'),
    path('concepts/<int:concept_id>/', concept_detail, name='concept_detail'),
    path('concepts/<int:concept_id>/edit', concept_edit, name='concept_edit'),
    path('concepts/<int:concept_id>/delete', concept_delete, name='concept_delete'),
    ########
    path('cash_boxes/create/', views.cash_box_create, name='cash_box_create'),
    path('cash_boxes/', views.cash_box_list, name='cash_box_list'),
    path('cash_boxes/<int:cash_box_id>/', views.cash_box_detail, name='cash_box_detail'),
    ########
    path('stampings/create/', views.stamping_create, name='stamping_create'),
    path('stampings/', views.stamping_list, name='stamping_list'),
    path('stampings/<int:stamping_id>/', views.stamping_detail, name='stamping_detail'),

]


