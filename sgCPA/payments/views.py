from datetime import datetime
from decimal import Decimal
from django.utils import timezone
from django.db.models import Count
import json



from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render

from attendances.models import Attendance, AttendanceStudent
from django.template.loader import render_to_string
from students.models import CourseDates, Student, Course
from xhtml2pdf import pisa

from .models import Concept, Payment, PaymentMethod, PaymentType, State, Fee, Enrollment, PaymentMethod2, CashBox, \
    Stamping, Invoice, InvoiceDetail, EnrollmentDetail
import calendar
from dateutil.relativedelta import relativedelta
from django.shortcuts import redirect,get_object_or_404
from django.urls import reverse

from .numero_letras import numero_a_letras
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def payments(request):
    payments = Payment.objects.all()

    pagination = Paginator(payments, 10)
    page = request.GET.get('page')

    try:
        payments = pagination.page(page)
    except PageNotAnInteger:
        payments = pagination.page(1)
    except EmptyPage:
        payments = pagination.page(pagination.num_pages)

    return render(request, 'payments.html', {'payments': payments})


def payment_detail(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    formated_payment_date = payment.payment_date.strftime('%Y-%m-%d')
    payment.payment_date = formated_payment_date
    invoice = Invoice.objects.get(id=payment.invoice.id)
    return render(request, 'payment_detail.html', {'payment': payment, 'invoice': invoice})


def search_pending_payments(request):
    if request.method == 'POST':

        cas_boxes = CashBox.objects.all()
        is_cash_boxes = False
        if cas_boxes and cas_boxes.first().stamping:
            is_cash_boxes = True

        student_ci = request.POST['student']
        student = Student.objects.filter(ciNumber=student_ci).first()

        if not student:
            return render(request, 'search_pending_payments.html', {'error': 'No se encontró un estudiante con ese número de cédula', 'is_cash_boxes': is_cash_boxes})

        return redirect('pending_payments', pk=student.id)

    else:
        cas_boxes = CashBox.objects.all()
        is_cash_boxes = False
        if cas_boxes and cas_boxes.first().stamping:
            is_cash_boxes = True

        return render(request, 'search_pending_payments.html', {'is_cash_boxes': is_cash_boxes})


def pending_payments(request, pk):
    if request.method == 'POST':
        student_ci = request.POST['student']
        student = Student.objects.get(ciNumber=student_ci)

        selected_fees = request.POST.getlist('selected_fees')
        selected_enrollment_details = request.POST.getlist('selected_enrollment_details')

        pending_fees = []
        pending_enrollment_details = []

        for fee_id in selected_fees:
            fee = Fee.objects.get(id=fee_id)
            pending_fees.append(fee)

        for enrollment_detail_id in selected_enrollment_details:
            enrollment_detail = EnrollmentDetail.objects.get(id=enrollment_detail_id)
            pending_enrollment_details.append(enrollment_detail)

        invoice = create_invoice(pending_fees, pending_enrollment_details, student, request.user)

        return redirect('show_payment_resume', pk=invoice.id)

    else:
        student = Student.objects.get(id=pk)
        pending_fees = Fee.objects.filter(student_id=pk, state_id=State.objects.get(name='pending').id)
        pending_enrollment_details = EnrollmentDetail.objects.filter(student_id=pk, state_id=State.objects.get(name='pending').id)

        return render(request, 'pending_payments.html', {'pending_fees': pending_fees, 'pending_enrollment_details': pending_enrollment_details, 'student': student})


def create_invoice(pending_fees, pending_enrollment_details, student, user):

    cash_box = CashBox.objects.get(active=True, user=user)

    invoice = Invoice()
    invoice.number = cash_box.stamping.actual_number
    cash_box.stamping.actual_number += 1
    cash_box.stamping.save()
    # complete the invoice last part with the 0 to the left, to complete the 7 characters
    invoice.name = str(cash_box.stamping.establishment_number) + '-' + str(cash_box.stamping.expedition_point) + '-' + str(cash_box.stamping.actual_number).zfill(7)
    invoice.date = datetime.now()
    invoice.amount = 0
    invoice.cash_box = cash_box
    invoice.stamping = cash_box.stamping
    invoice.valid_until = datetime.now() + relativedelta(months=1)
    invoice.client = student
    invoice.created_at = datetime.now()
    invoice.save()

    total_iva = 0

    for fee in pending_fees:
        invoice_detail = InvoiceDetail()
        invoice_detail.invoice = invoice
        invoice_detail.amount = fee.fee_amount
        invoice_detail.concept = Concept.objects.get(related_to='fee')
        invoice_detail.created_at = datetime.now()
        invoice_detail.fee = fee
        invoice_detail.save()

        invoice.amount += fee.fee_amount

        if invoice_detail.concept.iva == '10':
            invoice.iva_10 += fee.fee_amount * Decimal(str(0.1))
            invoice.sub_total_iva_10 += fee.fee_amount
        elif invoice_detail.concept.iva == '5':
            invoice.iva_5 += fee.fee_amount * Decimal(str(0.05))
            invoice.sub_total_iva_5 += fee.fee_amount
        else:
            invoice.sub_total_iva_0 += fee.fee_amount

    for enrollment_detail in pending_enrollment_details:
        invoice_detail = InvoiceDetail()
        invoice_detail.invoice = invoice
        invoice_detail.amount = enrollment_detail.amount
        invoice_detail.concept = Concept.objects.get(related_to='enrollment')
        invoice_detail.created_at = datetime.now()
        invoice_detail.enrollment_detail = enrollment_detail
        invoice_detail.save()

        invoice.amount += enrollment_detail.amount

        if invoice_detail.concept.iva == '10':
            invoice.iva_10 += enrollment_detail.amount * Decimal(str(0.1))
            invoice.sub_total_iva_10 += enrollment_detail.amount
        elif invoice_detail.concept.iva == '5':
            invoice.iva_5 += enrollment_detail.amount * Decimal(str(0.05))
            invoice.sub_total_iva_5 += enrollment_detail.amount
        else:
            invoice.sub_total_iva_0 += enrollment_detail.amount

    total_iva = invoice.iva_10 + invoice.iva_5
    invoice.iva_total = total_iva
    invoice.save()

    return invoice


def show_invoice(request, pk):
    if request.method == 'POST':
        invoice = Invoice.objects.get(id=pk)
        invoice.save()

        return redirect('payment_invoice_create', pk=pk)
    else:
        # Obtener la factura por ID, lanzando un error 404 si no se encuentra
        invoice = get_object_or_404(Invoice, id=pk)
        formatted_invoice_date = invoice.date.strftime('%Y-%m-%d')
        invoice.date = formatted_invoice_date
        # Obtener los detalles de la factura
        invoice_details = InvoiceDetail.objects.filter(invoice=invoice)

        is_invoice_paid = False
        payment = Payment.objects.filter(invoice=invoice).first()
        if payment:
            is_invoice_paid = True

        context = {
            'invoice': invoice,
            'invoice_details': invoice_details,
            'is_invoice_paid': is_invoice_paid
        }
        return render(request, 'show_invoice.html', context)


def show_payment_resume(request, pk):
    if request.method == 'POST':
        invoice = Invoice.objects.get(id=pk)
        invoice.save()

        return redirect('payment_invoice_create', pk=pk)
    else:
        # Obtener la factura por ID, lanzando un error 404 si no se encuentra
        invoice = get_object_or_404(Invoice, id=pk)
        formatted_invoice_date = invoice.date.strftime('%Y-%m-%d')
        invoice.date = formatted_invoice_date
        # Obtener los detalles de la factura
        invoice_details = InvoiceDetail.objects.filter(invoice=invoice)

        is_invoice_paid = False
        payment = Payment.objects.filter(invoice=invoice).first()
        if payment:
            is_invoice_paid = True

        context = {
            'invoice': invoice,
            'invoice_details': invoice_details,
            'is_invoice_paid': is_invoice_paid
        }
        return render(request, 'show_payment_resume.html', context)


def invoices(request):
    invoices = Invoice.objects.all()

    pagination = Paginator(invoices, 10)
    page = request.GET.get('page')

    try:
        invoices = pagination.page(page)
    except PageNotAnInteger:
        invoices = pagination.page(1)
    except EmptyPage:
        invoices = pagination.page(pagination.num_pages)

    return render(request, 'invoices.html', {'invoices': invoices})


def download_invoice(request, pk):
    invoice = Invoice.objects.get(id=pk)
    invoice_details = InvoiceDetail.objects.filter(invoice=invoice)

    invoice_amount_in_letters = numero_a_letras(invoice.amount)

    exentas = 0
    iva5 = 0
    iva10 = 0

    for invoice_detail in invoice_details:
        if invoice_detail.concept.iva == '10':
            iva10 += invoice_detail.amount
        elif invoice_detail.concept.iva == '5':
            iva5 += invoice_detail.amount
        else:
            exentas += invoice_detail.amount

    html = render_to_string('invoice_report.html', {'invoice': invoice, 'invoice_details': invoice_details,
                                                    'invoice_amount_in_letters': invoice_amount_in_letters, 'exentas': exentas, 'iva5': iva5, 'iva10': iva10})

    filename = 'invoice_' + str(invoice.name) + '.pdf'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}', status=500)
    return response


def payment_invoice_create(request, pk):
    if request.method == 'POST':

        invoice = Invoice.objects.get(id=pk)

        student_id = int(request.POST['student'])
        year = request.POST['year']
        payment_date = request.POST['payment_date']
        payment_method_id = int(request.POST['payment_method'])
        payment_type_id = PaymentType.objects.get(name='invoice').id
        payment_amount = float(request.POST['payment_amount'].replace(',', '.'))

        payment = Payment()
        payment.student_id = student_id
        payment.year = year
        payment.payment_date = payment_date
        payment.payment_method_id = payment_method_id
        payment.payment_type_id = payment_type_id
        payment.payment_amount = payment_amount
        payment.invoice = invoice
        payment.save()

        invoice_details = InvoiceDetail.objects.filter(invoice=invoice)

        for invoice_detail in invoice_details:
            if invoice_detail.fee:
                invoice_detail.fee.state = State.objects.get(name='paid')
                invoice_detail.fee.fee_paid_amount = invoice_detail.amount
                invoice_detail.fee.save()
            elif invoice_detail.enrollment_detail:
                invoice_detail.enrollment_detail.state = State.objects.get(name='paid')
                invoice_detail.enrollment_detail.paid_amount = invoice_detail.amount
                invoice_detail.enrollment_detail.save()

        return render(request, 'payment_detail.html', {'payment': payment, 'invoice': invoice})
    else:
        invoice = Invoice.objects.get(id=pk)
        student = Student.objects.get(id=invoice.client.id)
        payment_methods = PaymentMethod.objects.all()
        payment_types = PaymentType.objects.all()
        invoice = Invoice.objects.get(id=pk)
        payment_date = datetime.now()
        formatted_payment_date = payment_date.strftime('%Y-%m-%d')
        return render(request, 'payment_invoice_create.html', {'payment_methods': payment_methods,
                                                               'payment_types': payment_types, 'student': student, 'invoice': invoice,
                                                               'payment_amount': invoice.amount, 'payment_date': formatted_payment_date, 'year': datetime.now().year})


def fees(request):
    fees = Fee.objects.all()

    pagination = Paginator(fees, 10)
    page = request.GET.get('page')

    try:
        fees = pagination.page(page)
    except PageNotAnInteger:
        fees = pagination.page(1)
    except EmptyPage:
        fees = pagination.page(pagination.num_pages)

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


def create_fees(request, student_id, enrollment_detail_id):
    enrollment_detail = EnrollmentDetail.objects.get(id=enrollment_detail_id)
    course = Course.objects.get(id=enrollment_detail.enrollment.course.id)
    student = Student.objects.get(id=student_id)
    start_date = course.start_date
    end_date = course.end_date

    fees_quantity = calculate_fees_quantity(start_date, end_date)

    fee_amount = course.fee_amount

    for i in range(fees_quantity):
        fee = Fee()
        fee.student_id = student_id
        fee.year = course.year
        fee.fee_date = start_date
        fee.expiration_date = start_date + relativedelta(months=1)
        fee.fee_amount = fee_amount
        fee.state = State.objects.get(name='pending')
        fee.name = 'Cuota' + '/' + str(i + 1) + '/' + student.ciNumber + '/' + course.name
        fee.enrollment_detail = enrollment_detail
        fee.save()

        start_date = start_date + relativedelta(months=1)


def enrollments(request):
    enrollments = Enrollment.objects.all()
    return render(request, 'enrollments.html', {'enrollments': enrollments})


def enrollment_edit(request, enrollment_id):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        student = Student.objects.get(id=student_id)
        enrollment = Enrollment.objects.get(id=enrollment_id)
        course = Course.objects.get(id=enrollment.course.id)
        if student:
            enrollment_exists = EnrollmentDetail.objects.filter(
                student=student,
                enrollment__course=course
            ).exists()    
            if enrollment_exists:
                return JsonResponse({'message': 'Estudiante ya matriculado al curso'});
                
            else:
                if course.space_available > 0:
                    enrollment_details = EnrollmentDetail(
                        name='Matricula' + '/' + student.name,
                        enrollment=enrollment,
                        amount=enrollment.enrollment_amount,
                        student=student
                    )
                    enrollment_details.save()
                    course.space_available -= 1;
                    course.save()

                    create_fees(request, student_id, enrollment_details.id)

                    return JsonResponse({'message': 'Alumno matriculado correctamente'})
                else:
                    return JsonResponse({"message": 'Ya no hay cupos disponibles'})
        else:
            JsonResponse({"message": "No se encontraron estudiantes con ese número de cédula"}, status=404)
    else:    
        enrollment = Enrollment.objects.get(id=enrollment_id)
        has_fees = False
        # enrollment_details = EnrollmentDetail.objects.filter(enrollment=enrollment)
        # if Fee.objects.filter(enrollment_detail=enrollment_details.first()):
            # has_fees = True
        return render(request, 'enrollment_edit.html', {'enrollment': enrollment, 'has_fees': has_fees, 'enrollment_id': enrollment.id})



def enrollment_detail(request, enrollment_id):
    
    enrollment = Enrollment.objects.get(id=enrollment_id)
    enrollmentDetails = EnrollmentDetail.objects.filter(enrollment=enrollment)
    
    if request.method == 'POST':

        # Renderizar el template a HTML
        html = render_to_string('enrollment_detail_pdf.html', {'enrollments': enrollmentDetails})

        # # Crear un objeto de respuesta PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="matriculados_{enrollment.course.name}.pdf"'

        # Convertir HTML a PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse(f'Error al generar el PDF: {pisa_status.err}', status=500)
        return response
    else:    
        return render(request, 'enrollment_detail.html', {'enrollments': enrollmentDetails})


def enrollment_detail_payment(request, enrollment_id):
    enrollment = Enrollment.objects.get(id=enrollment_id)
    fees = Fee.objects.filter(enrollment=enrollment)
    if fees:
        return render(request, 'enrollment_detail_payment.html', {'enrollment': enrollment, 'fees': fees})


def enrollment_create(request):
    if request.method == 'POST':

        form_data = request.POST.dict()

        states = State.objects.all()

        course_id = form_data['course']
        enrollment_start_date = form_data['enrollment_start_date']
        enrollment_end_date = form_data['enrollment_end_date']
        # student_id = form_data['student_id']
        # student = Student.objects.get(id=student_id)

        # students = Student.objects.all()
        
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'El curso no existe'}, status=400)
        
        course = Course.objects.get(id=course_id)
        enrollment = Enrollment(
            name = 'Matricula' + '/' + course.name,
            course = course,
            enrollment_start_date = enrollment_start_date,
            enrollment_end_date = enrollment_end_date,
            enrollment_amount = course.enrollment_amount
        )
        
        enrollment.save()
        
        
        return JsonResponse({'id': enrollment.id});
        
        # for student in students:
            # studentId = request.POST.get(str(student.id))
            # if studentId  is not None and course.space_available > 0:
            #     enrollment.course_id = course_id
            #     # enrollment.enrollment_date = enrollment_date
            #     enrollment.state_id = states.get(name='pending').id
            #     enrollment.name = 'Matrícula' + '/' + student.ciNumber + '/' + course.name
            #     enrollment.student_id = studentId
            #     enrollment.enrollment_amount = course.enrollment_amount
            #     enrollment.save()
            #     courseDates = CourseDates.objects.filter(course=course)
                
            #     for courseDate in courseDates:
            #         attendance = Attendance.objects.filter(course_id=course_id, date=courseDate.date).first()
            #         AttendanceStudent.objects.create(attendance=attendance, student=student)
                    
            #     if course.space_available > 0:
            #         course.space_available -= 1
            #         course.save()

            #     create_fees(request, studentId, enrollment.id)
            #     enrollmentDetail = EnrollmentDetail(
            #         name
            #     )
                
                    
            # elif studentId is not None and course.space_available <= 0:
            #     # Si no hay cupos disponibles, maneja la situación de alguna forma adecuada
            #     return JsonResponse({"status": "error", "message": "No hay cupos disponibles para el curso"}, status=400)

        # return redirect(reverse('enrollment_create'))
    else:
        states = State.objects.all()
        students = Student.objects.all()
        fecha_actual = timezone.now().date()
    
    # Filtrar cursos cuyas fechas de inicio y fin de matriculación están en el rango de la fecha actual
        # courses = Course.objects.filter(
        #     enrollment_start_date__lte=fecha_actual,
        #     enrollment_end_date__gte=fecha_actual
        # )
        # courses = Course.objects.all()
        courses = Course.objects.annotate(num_enrollments=Count('enrollment')).filter(num_enrollments=0)
        return render(request, 'enrollment_create.html', {'states': states, 'students': students, 'courses': courses})

def enrollment_eliminar(request, id):
    
    enrollment = get_object_or_404(Enrollment, id=id)
    enrollment.active = False
    enrollment.save()
    return HttpResponse("Registro modificado correctamente")


def get_students(request, courseId):
    print(courseId)
    estudiantes_matriculados = Enrollment.objects.filter(course_id=courseId).values('student_id')
    estudiantes_no_matriculados = Student.objects.exclude(id__in=estudiantes_matriculados)
    print(estudiantes_no_matriculados)
    return JsonResponse({"Hola": "hola"})


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
        iva = request.POST.get('iva')
        related_to = request.POST.get('related_to')
        Concept.objects.create(name=name, description=description, iva=iva, related_to=related_to)
        return redirect('concept_list')
    return render(request, 'concept_create.html')


def concept_list(request):
    concepts = Concept.objects.all()

    paginator = Paginator(concepts, 10)
    page = request.GET.get('page')

    try:
        concepts = paginator.page(page)
    except PageNotAnInteger:
        concepts = paginator.page(1)
    except EmptyPage:
        concepts = paginator.page(paginator.num_pages)

    return render(request, 'concepts.html', {'concepts': concepts})


def concept_edit(request, concept_id):
    concept = get_object_or_404(Concept, id=concept_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        iva = request.POST.get('iva')
        related_to = request.POST.get('related_to')
        
        # Actualizar los campos del concepto
        concept.name = name
        concept.description = description
        concept.iva = iva
        concept.related_to = related_to
        
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


def cash_box_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        # created at the moment
        created_at = datetime.now()
        stamping = request.POST.get('stamping')
        stamping = Stamping.objects.get(id=stamping)
        # get logged in user
        user = request.user
        if request.POST.get('active') == 'true':
            active = True
        else:
            active = False

        CashBox.objects.create(name=name, description=description, created_at=created_at, stamping=stamping, user=user, active=active)
        return redirect('cash_box_list')

    else:
        stampings = Stamping.objects.all()
        return render(request, 'cash_box_create.html', {'stampings': stampings})


def cash_box_list(request):
    cash_boxes = CashBox.objects.all()
    is_cash_boxes = False
    if cash_boxes:
        is_cash_boxes = True
    return render(request, 'cash_boxes.html', {'cash_boxes': cash_boxes, 'is_cash_boxes': is_cash_boxes})


def cash_box_detail(request, cash_box_id):
    cash_box = CashBox.objects.get(id=cash_box_id)
    return render(request, 'cash_box_detail.html', {'cash_box': cash_box})


def stamping_create(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        valid_from = request.POST.get('valid_from')
        valid_until = request.POST.get('valid_until')
        establishment_number = request.POST.get('establishment_number')
        expedition_point = request.POST.get('expedition_point')
        start_number = request.POST.get('start_number')
        end_number = request.POST.get('end_number')
        actual_number = 1

        Stamping.objects.create(number=number, valid_from=valid_from, valid_until=valid_until, establishment_number=establishment_number, expedition_point=expedition_point, start_number=start_number, end_number=end_number, actual_number=actual_number)
        return redirect('stamping_list')
    else:
        return render(request, 'stamping_create.html')


def stamping_list(request):
    stampings = Stamping.objects.all()

    pagination = Paginator(stampings, 10)
    page = request.GET.get('page')

    try:
        stampings = pagination.page(page)
    except PageNotAnInteger:
        stampings = pagination.page(1)
    except EmptyPage:
        stampings = pagination.page(pagination.num_pages)

    return render(request, 'stampings.html', {'stampings': stampings})


def stamping_detail(request, stamping_id):
    stamping = Stamping.objects.get(id=stamping_id)
    return render(request, 'stamping_detail.html', {'stamping': stamping})