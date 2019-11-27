from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404,HttpResponse
from django.conf import settings
from principal.models import Usuario, Pelicula, Director
from principal.models import categoria as CategoriaTranslate


def sobre(request):
    html = "<html><body>Proyecto de ejemplo de vistas</body></htm>"
    return HttpResponse(html)


def inicio(request):
    return render(request,'inicio.html')


def usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})


def peliculas(request):
    peliculas = Pelicula.objects.all()
    res = dict({})
    for pelicula in peliculas:
        categoria = CategoriaTranslate[pelicula.categoria].value
        if categoria not in res.keys():
            res[categoria] = []
        list = res[categoria]
        if pelicula not in res.values():
            list.append(pelicula)
    return render(request, 'peliculas.html', {'peliculas': res})


def directores(request):
    directores = Director.objects.all()
    res = dict({})
    for director in directores:
        if director not in res.keys():
            res[director] = []
        list = res[director]
        print(director)
        list.append(Pelicula.objects.get(director=director))
    return render(request, 'directores.html', {'directores': res})