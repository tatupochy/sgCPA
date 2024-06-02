from django.shortcuts import render, Http404

from utils.utils import sendEmail
from .models import Country
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404



# Create your views here.
def registrar_pais(request):

    if(request.method == 'POST'):

        name = request.POST.get('name')
        code = request.POST.get('code')
        errors = {}
        values = {}
        
        # Verificar si ya existe un país con el mismo nombre o código
        if Country.objects.filter(name=name).exists():
            errors['country'] = 'El nombre del pais ya existe'
            values['country'] = name
        
        # if Country.objects.filter(code=code).exists():
        #     errors['code'] = 'El codigo ya existe'
        #     values['code'] = code
        
        if errors:            
            data = {
                'errors': errors,
                'values': values
            }
            return render(request, 'registrar_pais.html', data)
        
        

        newCountry = Country(
            name=name,
            code=code
        )

        newCountry.save()

        return HttpResponseRedirect('/listado_paises')
    else:
        return render(request, 'registrar_pais.html')


def listado_paises(request):

    country_list = Country.objects.filter(Q(active=True) | Q(active__isnull=True))
    page = request.GET.get('page', 1)
    
    has_results = country_list.exists()
    
    if not has_results:
        
        data = {
            'has_results': False,
            'param': id
        }
        return render(request, 'listado_paises.html', data)
    
    try:
        paginator = Paginator(country_list, 10)
        country_list = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': country_list,
        'paginator': paginator,
        'has_results': True
    }

    return render(request, 'listado_paises.html', data)

def buscar(request, name):
    
    country_list = Country.objects.filter(name__icontains=name, isActive=True)

    has_results = country_list.exists()
    
    if not has_results:
    
        data = {
            'has_results': False,
            'param': name
        }
        return render(request, 'listado_paises.html', data)
    
    
    page = request.GET.get('page', 1)
    paginator = Paginator(country_list, 10)
    
    try:
        countries = paginator.page(page)
    except PageNotAnInteger:
        countries = paginator.page(1)
    except EmptyPage:
        countries = paginator.page(paginator.num_pages)
    
    data = {
        'entity': countries,
        'paginator': paginator,
        'param': id,
        'has_results': True
    }
    
    return render(request, 'listado_paises.html', data)


def borrar_pais(request, id):
    if(request.method == 'GET'):
        country = get_object_or_404(Country, id=id)
        return render(request, 'borrar_pais.html', {'country': country})
    else:
        country = get_object_or_404(Country, id=id)
        country.active = False
        country.save()
        return HttpResponseRedirect('/listado_paises')
    
def editar_pais(request, id):
    if(request.method == 'GET'):
        country = get_object_or_404(Country, id=id)
        return render(request, 'registrar_pais.html', {'country': country})
    else:
        country = get_object_or_404(Country, id=id)
        name = request.POST.get('name')
        country.name = name
        country.save()
        return HttpResponseRedirect('/listado_paises')
        

