from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student

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
      
        
        
