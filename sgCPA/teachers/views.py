# teachers/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher
from django.http import JsonResponse
from cities.models import Cities
from countries.models import Country

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})

def teacher_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        birthDate = request.POST.get('birthDate')
        ciNumber = request.POST.get('ciNumber')
        phone = request.POST.get('phone')
        active = request.POST.get('active')
        city_id = request.POST.get('city')
        country_id = request.POST.get('country')

        teacher = Teacher.objects.create(
            name=name,
            lastName=lastName,
            email=email,
            birthDate=birthDate,
            ciNumber=ciNumber,
            phone=phone,
            active=active,
            city_id=city_id,
            country_id=country_id
        )
        return JsonResponse({'success': True, 'redirect_url': teacher.get_absolute_url()})
    else:
        city_list = Cities.objects.all()
        country_list = Country.objects.all()

        return render(request, 'teachers/teacher_form.html', {'city_list': city_list, 'country_list': country_list})

    return render(request, 'teachers/teacher_form.html')

def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.name = request.POST.get('name')
        teacher.lastName = request.POST.get('lastName')
        teacher.email = request.POST.get('email')
        teacher.birthDate = request.POST.get('birthDate')
        teacher.ciNumber = request.POST.get('ciNumber')
        teacher.phone = request.POST.get('phone')
        teacher.active = request.POST.get('active')
        teacher.city_id = request.POST.get('city')
        teacher.country_id = request.POST.get('country')
        teacher.save()
        return JsonResponse({'success': True, 'redirect_url': teacher.get_absolute_url()})
    return render(request, 'teachers/teacher_form.html', {'teacher': teacher})

def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return JsonResponse({'success': True, 'redirect_url': '/teachers/'})
    return render(request, 'teachers/teacher_confirm_delete.html', {'teacher': teacher})
