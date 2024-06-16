from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseRedirect

from countries.models import Country
from cities.models import Cities
from attendances.models import Attendance, AttendanceStudent
from payments.models import Enrollment
from utils.utils import calculate_class_days
from .models import CourseDates, Student, Course, Shift, Section
from subjects.models import Subject
from django.db.models import Q
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime
from teachers.models import Teacher


def registrar_alumno(request):
    if request.method == "GET":
        country_list = Country.objects.filter(Q(active=True) | Q(active__isnull=True))
        return render(request, 'students/registrar_alumno.html', {'country_list': country_list})
    
    form_data = request.POST.dict()

    
    city = Cities.objects.get(pk=form_data.get('city'))
    country = Country.objects.get(pk=form_data.get('country'))
    
    student = Student(
        name=form_data.get('name'),
        lastName=form_data.get('lastName'),
        email=form_data.get('email'),
        birthDate=form_data.get('birthDate'),
        ciNumber=form_data.get('ciNumber'),
        phone=form_data.get('phone'),
        city=city,
        country=country,
        fatherPhone=form_data.get('fatherPhone'),
        motherPhone=form_data.get('motherPhone'),
    )
    
    try:
        student.full_clean()
    except ValidationError as e:
        errors = e.message_dict
        data = {
            'country_list': country_list,
            'errors': errors
        }
        return render(request, 'students/registrar_alumno.html', data)

    student.save()
    return HttpResponseRedirect('/listado_alumnos')


def editar_alumno(request, id):
    

    if request.method == "GET":
        
        student = get_object_or_404(Student, id=id)
        country_list = Country.objects.filter(Q(active=True) | Q(active__isnull=True))
        city_list = Cities.objects.filter(country_id=id)
        data = {
            'student': student,
            'country_list': country_list,
            'city_list': city_list
        }
        return render(request, 'students/editar_alumno.html', data)
    else:
       student = get_object_or_404(Student, id=id)
       form_data = request.POST
       
       student.email = form_data.get('email')
       student.phone = form_data.get('phone')
       student.fatherPhone = form_data.get('fatherPhone')
       student.motherPhone = form_data.get('motherPhone')
       
       
        
       try:
          student.full_clean()
          student.save()  # Guardar los cambios en la base de datos
          return HttpResponseRedirect('/listado_alumnos')
       except ValidationError as e:
             errors = e.message_dict
             return HttpResponseBadRequest("Error en la validación: {}".format(errors))
        
        
def eliminar(request, id):
    student = get_object_or_404(Student, id=id)
    student.active = False
    student.save()
    return HttpResponse("Registro modificado correctamente")

def listado_alumnos(request):
    
    student_list = Student.objects.filter(Q(active=True) | Q(active__isnull=True))
    page = request.GET.get('page', 1)
    
    
    has_results = student_list.exists()
    
    if not has_results:
        # Si no se encuentra ningún estudiante, pasar un parámetro adicional al template
        data = {
            'has_results': False,
            'param': id
        }
        return render(request, 'students/listado_alumnos.html', data)
    
    try:
        paginator = Paginator(student_list, 10)
        student_list = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'entity': student_list,
        'paginator': paginator,
        'has_results': True
    }
        
    return render(request, 'students/listado_alumnos.html', data)

def buscar(request, id):
    # Realizar la búsqueda en el modelo Student
    student_list = Student.objects.filter(name__icontains=id) | Student.objects.filter(lastName__icontains=id)
    
    # Verificar si se encontraron estudiantes
    has_results = student_list.exists()
    
    if not has_results:
        # Si no se encuentra ningún estudiante, pasar un parámetro adicional al template
        data = {
            'has_results': False,
            'param': id
        }
        return render(request, 'students/listado_alumnos.html', data)
    
    # Realizar la paginación si se encuentran estudiantes
    page = request.GET.get('page', 1)
    paginator = Paginator(student_list, 10)
    
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    
    data = {
        'entity': students,
        'paginator': paginator,
        'param': id,
        'has_results': True
    }
    
    return render(request, 'students/listado_alumnos.html', data)
    

    


        


###### Cursos ######   
def registrar_curso(request):
    CHOICE_SHIFTS = Shift.objects.all()
    CHOICES_SECTIONS = Section.objects.all()

    if request.method == 'POST':
        subjects_ids = request.POST.getlist('subjects')
        name = request.POST.get('name')
        shift = Shift.objects.get(pk=request.POST.get('shift')) 
        section = Section.objects.get(pk=request.POST.get('section'))
        active =  request.POST.get('active') == 'on'  # Convertir a booleano
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        fee_amount = request.POST.get('fee_amount')
        days_per_week = request.POST.getlist('days_per_week')
        teacher = request.POST.get('teacher')
        minStudentsNumber = request.POST.get('minStudentsNumber')
        maxStudentsNumber = request.POST.get('maxStudentsNumber')
        enrollment_start_date = request.POST.get('enrollment_start_date')
        enrollment_end_date = request.POST.get('enrollment_end_date')
        enrollment_amount = request.POST.get('enrollment_amount')
        
        
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        class_days = list(map(int, days_per_week))

        teacher = Teacher.objects.get(pk=teacher)
        total_days, class_dates = calculate_class_days(start_date=start_date, end_date=end_date, class_days=class_days)
        
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
                year=datetime.datetime.now().year,
                teacher=teacher,
                minStudentsNumber=minStudentsNumber,
                maxStudentsNumber=maxStudentsNumber,
                enrollment_start_date=enrollment_start_date,
                enrollment_end_date=enrollment_end_date,
                enrollment_amount=enrollment_amount
            )
            # Guardar el curso en la base de datos
            curso.save()
            curso.subjects.add(*subjects_ids)
            for date in class_dates:
                CourseDates.objects.create(date=date, course=curso)
                attendance = Attendance.objects.create(date=date, course=curso)
               
           
            return redirect('detalle_curso', id=curso.id)
            
        else:
            # Si falta algún campo requerido, mostrar un mensaje de error o realizar alguna otra acción
            return HttpResponse("Faltan campos requeridos")
    else:
        subject_list = Subject.objects.filter(Q(active=True) | Q(active__isnull=True))
        teachers = Teacher.objects.filter(Q(active=True) | Q(active__isnull=True))
        return render(request, 'courses/registrar_curso.html', {'CHOICE_SHIFTS': CHOICE_SHIFTS, 'CHOICES_SECTIONS': CHOICES_SECTIONS, 'subject_list': subject_list, 'teachers': teachers})
    
def detalle_curso(request, id):
    curso = get_object_or_404(Course, pk= id)
    cursos = Course.objects.all()
    return render(request, 'courses/detalle_curso.html', {'curso': curso, 'cursos': cursos})

def editar_curso(request, id):
    curso = get_object_or_404(Course, pk=id)
    fechas = curso.coursedates_set.all()
    fechas_formateadas = [fecha.date.strftime("%A, %d de %B de %Y")  for fecha in fechas]
    print(fechas_formateadas)
    CHOICE_SHIFTS = Shift.objects.all()
    CHOICES_SECTIONS = Section.objects.all()
    if request.method == 'POST':
        subjects_ids = request.POST.getlist('subjects')
        name = request.POST.get('name')
        shift = Shift.objects.get(pk=request.POST.get('shift'))
        section = Section.objects.get(pk=request.POST.get('section'))
        active = request.POST.get('active') == 'on'
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        fee_amount = request.POST.get('fee_amount')
        days_per_week = request.POST.get('days_per_week')
        teacher = Teacher.objects.get(pk=request.POST.get('teacher'))

        if name and shift and start_date and end_date and fee_amount and days_per_week:
            # Actualizar los campos del curso con los nuevos valores
            curso.name = name
            curso.shift = shift
            curso.section = section
            curso.active = active
            curso.start_date = start_date
            curso.end_date = end_date
            curso.fee_amount = fee_amount
            curso.days_per_week = days_per_week
            curso.subjects.set(subjects_ids)
            curso.teacher = teacher
            curso.save()
            return redirect('detalle_curso', id=curso.id)
        else:
            return HttpResponse("Faltan campos requeridos")
    else:
        
        subject_list = Subject.objects.filter(Q(active=True) | Q(active__isnull=True))
        teachers = Teacher.objects.filter(Q(active=True) | Q(active__isnull=True))
        teacherSelected = curso.teacher
        
        curso.start_date = curso.start_date.strftime("%Y-%m-%d")
        curso.end_date = curso.end_date.strftime("%Y-%m-%d")
        ids_de_materias = list(curso.subjects.values_list('id', flat=True))
        
        data = {
            'CHOICE_SHIFTS': CHOICE_SHIFTS,
            'CHOICES_SECTIONS': CHOICES_SECTIONS,
            'curso': curso,
            'subject_list': subject_list,
            'ids_de_materias': ids_de_materias,
            'teachers': teachers,
            'teacherSelected': teacherSelected,
        }
        
        return render(request, 'courses/editar_curso.html', data)
    
def borrar_curso(request, id):
    curso = get_object_or_404(Course, pk=id)
    if request.method == 'POST':
        curso.delete()
        return redirect('listar_curso')
    return render(request, 'courses/borrar_curso.html', {'curso': curso})

def listar_curso(request):
    cursos = Course.objects.all()
    return render(request, 'courses/listar_curso.html', {'cursos': cursos})


def obtener_curso(request, id):
    
    course = Course.objects.get(id=id)
    
    # Verificar si hay algún registro de Enrollment para el curso
    if Enrollment.objects.filter(course_id=id).exists():
        # Si hay registros, obtener los estudiantes que no están matriculados en el curso
        estudiantes_matriculados = Enrollment.objects.filter(course_id=id).values('student_id')
        estudiantes_no_matriculados = Student.objects.exclude(id__in=estudiantes_matriculados)
    else:
        # Si no hay registros, obtener todos los estudiantes
        estudiantes_no_matriculados = Student.objects.all()
    
    # Convertir a lista de diccionarios para el JSON
    estudiantes_no_matriculados_list = list(estudiantes_no_matriculados.values('id', 'name', 'lastName', 'ciNumber'))
   
    
    data = {
        'enrollment_amount': course.enrollment_amount,
        'minStudentsNumber': course.minStudentsNumber,
        'maxStudentsNumber': course.maxStudentsNumber,
        'fee_amount': course.fee_amount,
        'minStudentsNumber': course.minStudentsNumber,
        'maxStudentsNumber': course.maxStudentsNumber,
        'student_list': estudiantes_no_matriculados_list,
        'space_available': course.space_available
        
    }
    return JsonResponse({"course_data":data})


###### Turnos ######   
def shift_list(request):
    shifts = Shift.objects.all()
    return render(request, 'shifts/shifts.html', {'shifts': shifts})


def shift_detail(request, id):
    shift = get_object_or_404(Shift, pk=id)
    return render(request, 'shifts/shift_detail.html', {'shift': shift})


def shift_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        active = request.POST.get('active') == 'on'
        description = request.POST.get('description')
        shift = Shift(name=name, active=active, description=description)
        shift.save()
        return redirect('shift_detail', id=shift.id)
    return render(request, 'shifts/shift_create.html')


def shift_edit(request, id):
    shift = get_object_or_404(Shift, pk=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        active = request.POST.get('active') == 'on'
        description = request.POST.get('description')
        shift.name = name
        shift.active = active
        shift.description = description
        shift.save()
        return redirect('shift_detail', id=shift.id)
    return render(request, 'shifts/shift_edit.html', {'shift': shift})


def shift_delete(request, id):
    shift = get_object_or_404(Shift, pk=id)
    shift.delete()
    return redirect('shift_list')


def section_list(request):
    sections = Section.objects.all()
    return render(request, 'sections/sections.html', {'sections': sections})


def section_detail(request, id):
    section = get_object_or_404(Section, pk=id)
    print('section_detail', section)
    return render(request, 'sections/section_detail.html', {'section': section})


def section_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        active = request.POST.get('active') == 'on'
        description = request.POST.get('description')
        section = Section(name=name, active=active, description=description)
        section.save()
        return redirect('section_detail', id=section.id)
    return render(request, 'sections/section_create.html')


def section_edit(request, id):
    section = get_object_or_404(Section, pk=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        active = request.POST.get('active') == 'on'
        description = request.POST.get('description')
        section.name = name
        section.active = active
        section.description = description
        section.save()
        return redirect('section_detail', id=section.id)
    return render(request, 'sections/section_edit.html', {'section': section})


def section_delete(request, id):
    section = get_object_or_404(Section, pk=id)
    section.delete()
    return redirect('section_list')