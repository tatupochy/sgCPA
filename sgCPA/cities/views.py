from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.db.models import Q
from countries.models import Country
from .models import Cities
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse


# Create your views here.
def registrar_ciudad(request):
    if(request.method == "GET"):
        country_list = Country.objects.filter(Q(active=True) | Q(active__isnull=True))
        data = {
            'country_list': country_list
        }
        
        return render(request, 'registrar_ciudad.html', data)
        
    else:
        form_data = request.POST.dict()
        country = Country.objects.get(pk=form_data.get('country'))
        name = form_data.get('name')
        
        city = Cities(
            name = name,
            country = country
        )
        
        city.save()
        
        return HttpResponseRedirect('/listado_ciudades')
    
def listado_ciudades(request):
    
    city_list = Cities.objects.filter(Q(active=True) | Q(active__isnull=True))
    
    paginator = Paginator(city_list, 10)
    
    data = {
        'entity': city_list,
        'paginator': paginator,
        'has_results': True
    }
    
    return render(request, 'listado_ciudades.html', data)

def borrar_ciudad(request, id):
    
    if(request.method == 'GET'):
        city = get_object_or_404(Cities, id=id)
        return render(request, 'borrar_ciudad.html', {'city': city})
    else:
        city = get_object_or_404(Cities, id=id)
        city.active = False
        city.save()
        return HttpResponseRedirect('/listado_ciudades')
    
def editar_ciudad(request, id):
     if(request.method == 'GET'):
        city = get_object_or_404(Cities, id=id)
        country_id = city.country.id
        country_list = Country.objects.filter(Q(active=True) | Q(active__isnull=True))
        
        data = {
            'city': city,
            'country_id': country_id,
            'country_list': country_list
        }
        return render(request, 'registrar_ciudad.html', data)
     else:
        city = get_object_or_404(Cities, id=id)
        name = request.POST.get('name')
        country_id = request.POST.get('country')
        country = get_object_or_404(Country, id=country_id)
        
        city.name = name
        city.country = country
        city.save()
        return HttpResponseRedirect('/listado_ciudades')
    
def obtener_ciudades_por_pais(request, id):
    ciudades = Cities.objects.filter(country_id=id, active=True)


    # Crear una lista para almacenar los datos de las ciudades
    ciudades_data = []

    # Iterar sobre las ciudades obtenidas y agregar sus datos a la lista
    for ciudad in ciudades:
        ciudad_data = {
            "id": ciudad.id,
            "name": ciudad.name,
            # Puedes agregar más campos si los necesitas
        }
        ciudades_data.append(ciudad_data)

    # Devolver la lista de datos de ciudades como una respuesta JSON
    return JsonResponse({"ciudades": ciudades_data})
        