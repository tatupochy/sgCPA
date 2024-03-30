from django.urls import path
from . import views
from .views import (
    payments,
    payment_detail,
    payment_create,
    fees,
    fee_detail,
    fee_create,
    enrollments,
    enrollment_detail,
    enrollment_create,
    create_fees
)


urlpatterns = [
    path('payments/', payments, name='payments'),
    path('payments/<int:payment_id>/', payment_detail, name='payment_detail'),
    path('payments/create/', payment_create, name='payment_create'),
    path('fees/', fees, name='fees'),
    path('fees/<int:fee_id>/', fee_detail, name='fee_detail'),
    path('fees/create/', fee_create, name='fee_create'),
    path('fees/create_fees/<int:student_id>', create_fees, name='create_fees'),
    path('enrollments/', enrollments, name='enrollments'),
    path('enrollments/<int:enrollment_id>/', enrollment_detail, name='enrollment_detail'),
    path('enrollments/create/', enrollment_create, name='enrollment_create'),
]