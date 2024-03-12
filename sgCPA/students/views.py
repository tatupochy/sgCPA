from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Student, Course
from .forms import CursoForm
import datetime

def registrar_alumno(request):    
    if(request.method == "GET"):
            return render(request, 'registrar_alumno.html')
    else:        
       form_data = request.POST.dict()

       student = Student(
            name=form_data.get('name', ''),
            lastName=form_data.get('lastName', ''),
            birthDate=form_data.get('birthDate', ''),
            inscriptionDate=form_data.get('inscriptionDate', ''),
            ciNumber=form_data.get('ciNumber', ''),
            phone=form_data.get('phone', ''),
            city=form_data.get('city', ''),
            fatherPhone=form_data.get('fatherPhone', ''),
            motherPhone=form_data.get('motherPhone', '')
       )
       
       student.save()

    
       return HttpResponse("enviado correctamente")

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