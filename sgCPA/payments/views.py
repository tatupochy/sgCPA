from django.shortcuts import render

from students.models import Student, Course
from .models import Concept, Payment, PaymentMethod, PaymentType, State, Fee, Enrollment, PaymentMethod2
import calendar
from dateutil.relativedelta import relativedelta
from django.shortcuts import redirect,get_object_or_404

# Create your views here.


def payments(request):
    payments = Payment.objects.all()
    return render(request, 'payments.html', {'payments': payments})


def payment_detail(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    formated_payment_date = payment.payment_date.strftime('%Y-%m-%d')
    payment.payment_date = formated_payment_date
    return render(request, 'payment_detail.html', {'payment': payment})


def payment_create(request):
    if request.method == 'POST':
        student_id = int(request.POST['student'])
        year = request.POST['year']
        payment_date = request.POST['payment_date']
        payment_method_id = int(request.POST['payment_method'])
        payment_type_id = int(request.POST['payment_type'])
        payment_amount = int(request.POST['payment_amount'])

        payment = Payment()
        payment.student_id = student_id
        payment.year = year
        payment.payment_date = payment_date
        payment.payment_method_id = payment_method_id
        payment.payment_type_id = payment_type_id
        payment.payment_amount = payment_amount
        payment.save()

        if payment.payment_type_id == 1:
            enrollment_id = int(request.POST['enrollment'])
            enrollment = Enrollment.objects.get(id=enrollment_id)
            enrollment.enrollment_paid_amount = enrollment.enrollment_paid_amount + payment_amount
            if enrollment.enrollment_paid_amount == enrollment.enrollment_amount and enrollment.enrollment_paid_amount != 0:
                enrollment.state_id = State.objects.get(name='paid')
            elif enrollment.enrollment_amount > enrollment.enrollment_paid_amount and enrollment.enrollment_paid_amount != 0:
                enrollment.state_id = State.objects.get(name='partial')
            elif enrollment.enrollment_paid_amount == 0:
                enrollment.state_id = State.objects.get(name='pending')

            enrollment.save()

        elif payment.payment_type_id == 2:
            fee_id = int(request.POST['fee'])
            fee = Fee.objects.get(id=fee_id)
            fee.fee_paid_amount = fee.fee_paid_amount + payment_amount
            if fee.fee_paid_amount == fee.fee_amount and fee.fee_paid_amount != 0:
                fee.state_id = State.objects.get(name='paid')
            elif fee.fee_amount > fee.fee_paid_amount and fee.fee_paid_amount != 0:
                fee.state_id = State.objects.get(name='partial')
            elif fee.fee_paid_amount == 0:
                fee.state_id = State.objects.get(name='pending')

            fee.save()

        return render(request, 'payments.html', {'payments': Payment.objects.all()})
    else:
        payment_methods = PaymentMethod.objects.all()
        payment_types = PaymentType.objects.all()
        students = Student.objects.all()
        fees = Fee.objects.all()
        enrollments = Enrollment.objects.all()
        return render(request, 'payment_create.html', {'payment_methods': payment_methods, 'payment_types': payment_types, 'students': students, 'fees': fees, 'enrollments': enrollments})


def payment_fee_create(request, pk):
    if request.method == 'POST':
        student_id = int(request.POST['student'])
        year = request.POST['year']
        payment_date = request.POST['payment_date']
        payment_method_id = int(request.POST['payment_method'])
        payment_type_id = PaymentType.objects.get(name='fee').id
        payment_amount = int(request.POST['payment_amount'])

        payment = Payment()
        payment.student_id = student_id
        payment.year = year
        payment.payment_date = payment_date
        payment.payment_method_id = payment_method_id
        payment.payment_type_id = payment_type_id
        payment.payment_amount = payment_amount
        payment.save()

        fee = Fee.objects.get(id=pk)
        fee.fee_paid_amount = fee.fee_paid_amount + payment_amount
        if fee.fee_paid_amount == fee.fee_amount and fee.fee_paid_amount != 0:
            fee.state_id = State.objects.get(name='paid')
        elif fee.fee_amount > fee.fee_paid_amount and fee.fee_paid_amount != 0:
            fee.state_id = State.objects.get(name='partial')
        elif fee.fee_paid_amount == 0:
            fee.state_id = State.objects.get(name='pending')

        fee.save()

        return render(request, 'payments.html', {'payments': Payment.objects.all()})
    else:
        fee = Fee.objects.get(id=pk)
        student = Student.objects.get(id=fee.student_id)
        payment_methods = PaymentMethod.objects.all()
        payment_types = PaymentType.objects.all()
        students = Student.objects.all()
        fee = Fee.objects.get(id=pk)
        return render(request, 'payment_fee_create.html', {'payment_methods': payment_methods, 'payment_types': payment_types, 'student': student, 'fee': fee})


def payment_enrollment_create(request, pk):
    if request.method == 'POST':
        student_id = int(request.POST['student'])
        year = request.POST['year']
        payment_date = request.POST['payment_date']
        payment_method_id = int(request.POST['payment_method'])
        payment_type_id = PaymentType.objects.get(name='enrollment').id
        payment_amount = int(request.POST['payment_amount'])

        payment = Payment()
        payment.student_id = student_id
        payment.year = year
        payment.payment_date = payment_date
        payment.payment_method_id = payment_method_id
        payment.payment_type_id = payment_type_id
        payment.payment_amount = payment_amount
        payment.save()

        enrollment = Enrollment.objects.get(id=pk)
        enrollment.enrollment_paid_amount = enrollment.enrollment_paid_amount + payment_amount
        if enrollment.enrollment_paid_amount == enrollment.enrollment_amount and enrollment.enrollment_paid_amount != 0:
            enrollment.state_id = State.objects.get(name='paid')
        elif enrollment.enrollment_amount > enrollment.enrollment_paid_amount and enrollment.enrollment_paid_amount != 0:
            enrollment.state_id = State.objects.get(name='partial')
        elif enrollment.enrollment_paid_amount == 0:
            enrollment.state_id = State.objects.get(name='pending')

        enrollment.save()

        return render(request, 'payments.html', {'payments': Payment.objects.all()})
    else:
        enrollment = Enrollment.objects.get(id=pk)
        student = Student.objects.get(id=enrollment.student_id)
        payment_methods = PaymentMethod.objects.all()
        payment_types = PaymentType.objects.all()
        students = Student.objects.all()
        enrollment = Enrollment.objects.get(id=pk)
        return render(request, 'payment_enrollment_create.html', {'payment_methods': payment_methods, 'payment_types': payment_types, 'student': student, 'enrollment': enrollment})


def fees(request):
    fees = Fee.objects.all()
    for fee in fees:
        if fee.is_overdue():
            fee.state = State.objects.get(name='overdue')
            fee.save()
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
    

def calculate_fees_quantity(start_date, end_date):
    difference = relativedelta(end_date, start_date)
    total_months = difference.years * 12 + difference.months + 1
    return total_months


def create_fees(request, student_id):
    enrollment = Enrollment.objects.get(student_id=student_id)
    course = enrollment.course
    student = Student.objects.get(id=student_id)
    start_date = enrollment.enrollment_date
    end_date = course.end_date

    fees_quantity = calculate_fees_quantity(start_date, end_date)

    fee_amount = enrollment.course.fee_amount

    for i in range(fees_quantity):
        fee = Fee()
        fee.student_id = student_id
        fee.year = course.year
        fee.fee_date = start_date
        fee.expiration_date = start_date + relativedelta(months=1)
        fee.fee_amount = fee_amount
        fee.state = State.objects.get(name='pending')
        fee.name = 'Cuota' + '/' + str(i + 1) + '/' + student.ciNumber
        fee.save()

        start_date = start_date + relativedelta(months=1)

    fees = Fee.objects.all()

    return render(request, 'fees.html', {'fees': fees})


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

        student_ci = form_data['student']
        course_id = form_data['course']
        year = form_data['year']
        enrollment_date = form_data['enrollment_date']
        amount = form_data['enrollment_amount']

        student = Student.objects.get(ciNumber=student_ci)
        student_id = student.id
        course = Course.objects.get(id=course_id)

        enrollment = Enrollment()
        enrollment.student_id = student_id
        enrollment.course_id = course_id
        enrollment.year = year
        enrollment.enrollment_date = enrollment_date
        print('amount', amount)
        enrollment.enrollment_amount = amount
        enrollment.state_id = states.get(name='pending').id
        enrollment.name = 'Matrícula' + '/' + student.ciNumber + '/' + course.name
        enrollment.save()

        return render(request, 'enrollment_detail.html', {'enrollment': enrollment})
    else:
        states = State.objects.all()
        students = Student.objects.all()
        courses = Course.objects.all()
        return render(request, 'enrollment_create.html', {'states': states, 'students': students, 'courses': courses})
    

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


####################################################

def payment_method_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name == 'custom':
            name = request.POST.get('custom_name')
        description = request.POST.get('description')
        PaymentMethod2.objects.create(name=name, description=description)
        return redirect('payment_method_list')
    return render(request, 'payment_method_form.html')

def payment_method_list(request):
    payment_methods = PaymentMethod2.objects.all()
    return render(request, 'payment_method_list.html', {'payment_methods': payment_methods})

def payment_method_edit(request, payment_method_id):
    payment_method = get_object_or_404(PaymentMethod2, id=payment_method_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        
        # Actualizar los campos del método de pago
        payment_method.name = name
        payment_method.description = description
        payment_method.status = bool(status)  # Convertir a booleano
        
        # Guardar los cambios en la base de datos
        payment_method.save()
        
        return redirect('payment_method_list')  # Redireccionar a la lista de métodos de pago después de editar
        
    return render(request, 'payment_method_edit.html', {'payment_method': payment_method})

def payment_method_delete(request, payment_method_id):
    payment_method = get_object_or_404(PaymentMethod2, id=payment_method_id)
    if request.method == 'POST':
        payment_method.delete()
        return redirect('payment_method_list')  # Redirect to the payment method list after deletion
    return render(request, 'payment_method_delete.html', {'payment_method': payment_method})

def concept_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Concept.objects.create(name=name, description=description)
        return redirect('concept_list')
    return render(request, 'concept_create.html')

def concept_list(request):
    concepts = Concept.objects.all()
    return render(request, 'concepts.html', {'concepts': concepts})

def concept_edit(request, concept_id):
    concept = get_object_or_404(Concept, id=concept_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        # Actualizar los campos del concepto
        concept.name = name
        concept.description = description
        
        # Guardar los cambios en la base de datos
        concept.save()
        
        return redirect('concept_list')  # Redireccionar a la lista de conceptos después de editar
        
    return render(request, 'concept_edit.html', {'concept': concept})

def concept_delete(request, concept_id):
    concept = get_object_or_404(Concept, pk=concept_id)
    
    concept.delete()

    return redirect('concept_list')

def concept_detail(request, concept_id):
    concept = Concept.objects.get(id=concept_id)
    return render(request, 'concept_detail.html', {'concept': concept})

