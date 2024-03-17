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
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.year = datetime.datetime.now().year
            curso.save()
            return redirect('detalle_curso', curso_id=curso.id)
    else:
        form = CursoForm()
    return render(request, 'registrar_curso.html', {'form': form})



def detalle_curso(request, id):
    curso = get_object_or_404(Course, pk= id)
    return render(request, 'detalle_curso.html', {'curso': curso})
