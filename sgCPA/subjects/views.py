from django.shortcuts import redirect, render, Http404, HttpResponse, get_object_or_404
from django.core.exceptions import ValidationError
from .models import Subject
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
# Create your views here.

def registrar_materia(request):
    if(request.method == "POST"):
        form_data = request.POST.dict()
        name = form_data.get('name')
        
        subject = Subject(name=name)
        
        try:
            subject.full_clean()
        except ValidationError as e:
             errors = e.message_dict
             responseMessage = {
                'error': 'Este campo no puede estar vacio'
             }
             return render(request, 'subjects/create_subject.html', responseMessage)
         
        subject.save()
        # redirect('/listado_')
        responseMessage = {
            'success': 'Materia creada correctamente' 
        }
        return redirect('/listado_materias')
        # return render(request, 'subjects/create_subject.html', responseMessage)

    return render(request, 'subjects/create_subject.html')


def listado_materias(request):
     subject_list = Subject.objects.filter(Q(active=True) | Q(active__isnull=True))
     page = request.GET.get('page', 1)
    
    
     has_results = subject_list.exists()
    
     if not has_results:
        # Si no se encuentra ningún estudiante, pasar un parámetro adicional al template
        data = {
            'has_results': False,
            'param': id
        }
        return render(request, 'subjects/subject_list.html', data)
    
     try:
         paginator = Paginator(subject_list, 10)
         subject_list = paginator.page(page)
     except:
        raise Http404
    
     data = {
        'entity': subject_list,
        'paginator': paginator,
        'has_results': True
    }
        
     return render(request, 'subjects/subject_list.html', data)
 
def listado_materias_buscar(request, name):
    subject_list = Subject.objects.filter(name__icontains=name)
    
    # Verificar si se encontraron estudiantes
    has_results = subject_list.exists()
    
    if not has_results:
        # Si no se encuentra ningún estudiante, pasar un parámetro adicional al template
        data = {
            'has_results': False,
            'param': name
        }
        return render(request, 'subjects/subject_list.html', data)
    
    # Realizar la paginación si se encuentran materias
    page = request.GET.get('page', 1)
    paginator = Paginator(subject_list, 10)
    
    try:
        subject_list = paginator.page(page)
    except PageNotAnInteger:
        subject_list = paginator.page(1)
    except EmptyPage:
        subject_list = paginator.page(paginator.num_pages)
    
    data = {
        'entity': subject_list,
        'paginator': paginator,
        'param': name,
        'has_results': True
    }
    
    return render(request, 'subjects/subject_list.html', data)
 
 
 
def editar_materia(request, id):
    if(request.method == "GET"):
        subject = Subject.objects.get(pk=id)
        data = {
            'subject': subject
        }
        return render(request, 'subjects/create_subject.html', data)
    else:
        subject = get_object_or_404(Subject, id=id)
        form_data = request.POST
        
        subject.name = form_data.get('name')
        
        
        
        try:
            subject.full_clean()
        except ValidationError as e:
             errors = e.message_dict
             responseMessage = {
                'error': 'Este campo no puede estar vacio'
             }
             return render(request, 'subjects/create_subject.html', responseMessage)
         
        subject.save()
        responseMessage = {
            'success': 'Materia actualizada correctamente' 
        }
        return redirect('/listado_materias')
    
def eliminar_materia(request, id):
    subject = get_object_or_404(Subject, id=id)
    subject.active = False
    subject.save()
    return render(request, 'subjects/subject_list.html')