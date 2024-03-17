from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponse
from .models import Student, Course
from .forms import CursoForm
import datetime

def registrar_alumno(request):
    if request.method == "GET":
        return render(request, 'registrar_alumno.html')
    
    form_data = request.POST.dict()

    student = Student(
        name=form_data.get('name'),
        lastName=form_data.get('lastName'),
        email=form_data.get('email'),
        birthDate=form_data.get('birthDate'),
        inscriptionDate=form_data.get('inscriptionDate'),
        ciNumber=form_data.get('ciNumber'),
        phone=form_data.get('phone'),
        city=form_data.get('city'),
        fatherPhone=form_data.get('fatherPhone'),
        motherPhone=form_data.get('motherPhone')
    )
    
    try:
        student.full_clean()
    except ValidationError as e:
        errors = e.message_dict
        return HttpResponseBadRequest("Error en la validación: {}".format(errors))

    student.save()
    return HttpResponse("Enviado correctamente")

###### Cursos ######   
def registrar_curso(request):
    CHOICE_SHIFTS = Course.CHOICE_SHIFTS
    CHOICES_SECTIONS = Course.CHOICES_SECTIONS

    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        shift = request.POST.get('shift')
        section = request.POST.get('section')
        active =  request.POST.get('active') == 'on'  # Convertir a booleano
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        fee_amount = request.POST.get('fee_amount')
        days_per_week = request.POST.get('days_per_week')

        # Verificar si todos los campos requeridos están presentes
        if name and shift and start_date and end_date and fee_amount and days_per_week:
            # Crear una instancia de Course
            curso = Course(
                name=name,
                shift=shift,
                section=section,
                active=active,
                start_date=start_date,
                end_date=end_date,
                fee_amount=fee_amount,
                days_per_week=days_per_week,
                year=datetime.datetime.now().year
            )
            # Guardar el curso en la base de datos
            curso.save()
            return redirect('detalle_curso', id=curso.id)
        else:
            # Si falta algún campo requerido, mostrar un mensaje de error o realizar alguna otra acción
            return HttpResponse("Faltan campos requeridos")
    else:
        return render(request, 'registrar_curso.html', {'CHOICE_SHIFTS': CHOICE_SHIFTS, 'CHOICES_SECTIONS': CHOICES_SECTIONS})
    
def detalle_curso(request, id):
    curso = get_object_or_404(Course, pk= id)
    cursos = Course.objects.all()
    return render(request, 'detalle_curso.html', {'curso': curso, 'cursos': cursos})
