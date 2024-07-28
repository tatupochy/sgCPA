# teachers/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher
from django.http import JsonResponse
from cities.models import Cities
from countries.models import Country
from accounts.models import Person
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def teacher_list(request):
    teachers = Teacher.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(teachers, 5)

    try:
        teachers = paginator.page(page)
    except PageNotAnInteger:
        teachers = paginator.page(1)
    except EmptyPage:
        teachers = paginator.page(paginator.num_pages)

    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})

def teacher_create(request):
    if request.method == 'POST':

        country = Country.objects.get(pk=request.POST.get('country_id'))
        city = Cities.objects.get(pk=request.POST.get('city_id'))

        name = request.POST.get('name')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        birthDate = request.POST.get('birthDate')
        ciNumber = request.POST.get('ciNumber')
        phone = request.POST.get('phone')
        active = request.POST.get('active')
        city_id = city
        country_id = country

        # crear persona
        person = Person(name=name, last_name=lastName, email=email, birth_date=birthDate, ci=ciNumber, phone=phone, city=city_id, country=country_id)

        teacher = Teacher(name=name, lastName=lastName, email=email, birthDate=birthDate, ciNumber=ciNumber, phone=phone, active=active, city=city_id, country=country_id)
        teacher.save()
        person.teacher = teacher
        person.save()
        return redirect('teacher_list')
    else:
        city_list = Cities.objects.all()
        country_list = Country.objects.all()

        return render(request, 'teachers/teacher_form.html', {'city_list': city_list, 'country_list': country_list})

    #return render(request, 'teachers/teacher_form.html')

def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':

        form_data = request.POST.copy()

        country = Country.objects.get(pk=request.POST.get('country_id'))
        city = Cities.objects.get(pk=request.POST.get('city_id'))

        teacher.name = request.POST.get('name')
        teacher.lastName = request.POST.get('lastName')
        teacher.email = request.POST.get('email')
        teacher.birthDate = request.POST.get('birthDate')
        teacher.ciNumber = request.POST.get('ciNumber')
        teacher.phone = request.POST.get('phone')
        teacher.city_id = city
        teacher.country_id = country

        if 'active' in form_data:
            if form_data['active'] == 'on':
                teacher.active = True
            else:
                teacher.active = False
        else:
            teacher.active = False

        teacher.save()

        # actualizar persona
        person = Person.objects.get(teacher=teacher)
        person.name = request.POST.get('name')
        person.last_name = request.POST.get('lastName')
        person.email = request.POST.get('email')
        person.birth_date = request.POST.get('birthDate')
        person.ci = request.POST.get('ciNumber')
        person.phone = request.POST.get('phone')
        person.city = city
        person.country = country
        person.save()

        return JsonResponse({'success': True, 'redirect_url': teacher.get_absolute_url()})
    else:
        formatted_birthDate = teacher.birthDate.strftime('%Y-%m-%d')
        teacher.birthDate = formatted_birthDate
        return render(request, 'teachers/teacher_edit.html', {'teacher': teacher})

def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    # check if there are any courses related to this teacher
    if teacher.course_set.all():
        return render(request, 'teachers/teacher_error.html', {'error': 'Este profesor tiene cursos asignados, no se puede eliminar.'})
    teacher.delete()

    return render(request, 'teachers/teacher_list.html', {'teachers': Teacher.objects.all()})
