from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404,HttpResponse
from django.conf import settings


def sobre(request):
    html = "<html><body>Proyecto de ejemplo de vistas</body></htm>"
    return HttpResponse(html)


def inicio(request):
    return render(request,'inicio.html')


def usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})
