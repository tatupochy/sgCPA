from django.shortcuts import render
from .models import Country
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404



# Create your views here.
def registrar_pais(request):

    if(request.method == 'POST'):

        name = request.POST.get('name')

        newCountry = Country(
            name=name,
        )

        newCountry.save()

        return HttpResponseRedirect('/listado_paises')
    else:
        return render(request, 'registrar_pais.html')


def listado_paises(request):

    country_list = Country.objects.filter(Q(active=True) | Q(active__isnull=True))

    paginator = Paginator(country_list, 10)


    data = {
        'entity': country_list,
        'paginator': paginator,
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
        

