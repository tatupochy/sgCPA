from django.shortcuts import render

from students.models import Student
from .models import Payment, PaymentMethod, PaymentType, State, Fee, Enrollment
import calendar
from dateutil.relativedelta import relativedelta

# Create your views here.


def payments(request):
    payments = Payment.objects.all()
    return render(request, 'payments.html', {'payments': payments})


def payment_detail(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    return render(request, 'payment_detail.html', {'payment': payment})


def payment_create(request):
    if request.method == 'POST':
        student_id = request.POST['student']
        year = request.POST['year']
        payment_date = request.POST['payment_date']
        payment_method_id = request.POST['payment_method']
        payment_type_id = request.POST['payment_type']
        amount = request.POST['amount']

        payment = Payment()
        payment.student_id = student_id
        payment.year = year
        payment.payment_date = payment_date
        payment.payment_method_id = payment_method_id
        payment.payment_type_id = payment_type_id
        payment.amount = amount
        payment.save()

        return render(request, 'payment_created.html', {'payment': payment})
    else:
        payment_methods = PaymentMethod.objects.all()
        payment_types = PaymentType.objects.all()
        students = Student.objects.all()
        fees = Fee.objects.all()
        enrollments = Enrollment.objects.all()
        return render(request, 'payment_create.html', {'payment_methods': payment_methods, 'payment_types': payment_types, 'students': students, 'fees': fees, 'enrollments': enrollments})
    

def fees(request):
    fees = Fee.objects.all()
    return render(request, 'fees.html', {'fees': fees})


def fee_detail(request, fee_id):
    fee = Fee.objects.get(id=fee_id)
    return render(request, 'fee_detail.html', {'fee': fee})


def fee_create(request):
    if request.method == 'POST':
        student_id = request.POST['student']
        year = request.POST['year']
        fee_date = request.POST['fee_date']
        expiration_date = request.POST['expiration_date']
        amount = request.POST['amount']
        state_id = request.POST['state']

        fee = Fee()
        fee.student_id = student_id
        fee.year = year
        fee.fee_date = fee_date
        fee.expiration_date = expiration_date
        fee.amount = amount
        fee.state_id = state_id
        fee.save()

        return render(request, 'fee_created.html', {'fee': fee})
    else:
        states = State.objects.all()
        return render(request, 'fee_create.html', {'states': states})
    

def create_fees(request, student_id):
    enrollment = Enrollment.objects.get(student_id=student_id)
    course = enrollment.course

    start_date = enrollment.enrollment_date
    end_date = course.end_date

    fees_quantity = calculate_fees_quantity(start_date, end_date)

    fee_amount = enrollment.enrollment_amount

    for i in range(fees_quantity):
        fee = Fee()
        fee.student_id = student_id
        fee.year = course.year
        fee.fee_date = start_date
        fee.expiration_date = start_date
        fee.fee_amount = fee_amount
        fee.state = State.objects.get(name='pending').id
        fee.save()

        start_date = start_date + relativedelta(months=1)

    return render(request, 'fees.html')


def calculate_fees_quantity(start_date, end_date):

    start_year, month_start = start_date.year, start_date.month
    end_year, month_end = end_date.year, end_date.month

    difference = (end_year - start_year) * 12 + (month_end - month_start) + 1

    quantity = 0

    for i in range(difference):
        last_day = calendar.monthrange(start_year, month_start)[1]

        if start_date.day == last_day:
            quantity += 1

        month_start += 1
        if month_start > 12:
            month_start = 1
            start_year += 1

    return quantity

def enrollments(request):
    enrollments = Enrollment.objects.all()
    return render(request, 'enrollments.html', {'enrollments': enrollments})


def enrollment_detail(request, enrollment_id):
    enrollment = Enrollment.objects.get(id=enrollment_id)
    return render(request, 'enrollment_detail.html', {'enrollment': enrollment})


def enrollment_create(request):
    if request.method == 'POST':

        form_data = request.POST.dict()
        print('form_data', form_data)

        states = State.objects.all()

        student_id = form_data['student']
        year = form_data['year']
        enrollment_date = form_data['enrollment_date']
        amount = form_data['enrollment_amount']

        enrollment = Enrollment()
        enrollment.student_id = student_id
        enrollment.year = year
        enrollment.enrollment_date = enrollment_date
        print('amount', amount)
        enrollment.enrollment_amount = amount
        enrollment.state_id = states.get(name='pending').id
        enrollment.save()

        return render(request, 'enrollments.html', {'enrollment': enrollment})
    else:
        states = State.objects.all()
        students = Student.objects.all()
        return render(request, 'enrollment_create.html', {'states': states, 'students': students})
    

def payment_methods(request):
    payment_methods = PaymentMethod.objects.all()
    return render(request, 'payment_methods.html', {'payment_methods': payment_methods})


def payment_method_detail(request, payment_method_id):
    payment_method = PaymentMethod.objects.get(id=payment_method_id)
    return render(request, 'payment_method_detail.html', {'payment_method': payment_method})


def payment_method_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']

        payment_method = PaymentMethod()
        payment_method.name = name
        payment_method.description = description
        payment_method.save()

        return render(request, 'payment_method_created.html', {'payment_method': payment_method})
    else:
        return render(request, 'payment_method_create.html')
    

def payment_types(request):
    payment_types = PaymentType.objects.all()
    return render(request, 'payment_types.html', {'payment_types': payment_types})


def payment_type_detail(request, payment_type_id):
    payment_type = PaymentType.objects.get(id=payment_type_id)
    return render(request, 'payment_type_detail.html', {'payment_type': payment_type})


def payment_type_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']

        payment_type = PaymentType()
        payment_type.name = name
        payment_type.description = description
        payment_type.save()

        return render(request, 'payment_type_created.html', {'payment_type': payment_type})
    else:
        return render(request, 'payment_type_create.html')
    

def states(request):
    states = State.objects.all()
    return render(request, 'states.html', {'states': states})


def state_detail(request, state_id):
    state = State.objects.get(id=state_id)
    return render(request, 'state_detail.html', {'state': state})


