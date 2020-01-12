from django.shortcuts import render
from django.db import models
from django.db.models import F, Q, Exists, Value, IntegerField, Sum
from .models import Artista, UsuarioEtiquetaArtista, Usuario, UsuarioArtista, Etiqueta
import csv
import datetime as dt
from collections import Counter
import itertools
from django.conf import settings
from .forms import user_id_form
#Populate Methods

data_path = "./data/"


def populate(request):
    print("Populate")
    populate_artists()
    populate_tags()
    populate_users()
    populate_user_artists()
    populate_user_taggedartists()
    artist_profile()

    print(UsuarioArtista.objects.filter(usuario_id=2).first().tiempoEscucha )

    return render(request, 'index.html')


def populate_tags():
    Etiqueta.objects.all().delete()
    with open(data_path + "tags.dat", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)
        list_to_create = [Etiqueta(idTag=row[0], tagValue=row[1]) for row in csv_reader]
    Etiqueta.objects.bulk_create(list_to_create)
    print("Tags populated")
    
    
def populate_artists():
    Artista.objects.all().delete()
    with open(data_path + "artists.dat", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)
        list_to_create = [Artista(idArtista=row[0], nombre=row[1], url=row[2], pictureUrl=row[3]) for row in csv_reader]
    Artista.objects.bulk_create(list_to_create)
    print("Artistas populated")


def populate_users():
    Usuario.objects.all().delete()
    Usuario.objects.bulk_create([Usuario(idUsuario=i) for i in range(2101)])
    print("Users populated")


def populate_user_artists():
    UsuarioArtista.objects.all().delete()
    with open(data_path + "user_artists.dat", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)
        list_to_create = []
        for row in csv_reader:
            print(row)
            try:
                ua = UsuarioArtista(usuario=Usuario.objects.get(idUsuario=row[0]),
                                    artista=Artista.objects.get(idArtista=row[1]),
                                    tiempoEscucha=row[2])
                list_to_create.append(ua)
            except:
                pass

    UsuarioArtista.objects.bulk_create(list_to_create)
    print("User_Artists populated")


def populate_user_taggedartists():
    UsuarioEtiquetaArtista.objects.all().delete()
    with open(data_path + "user_taggedartists.dat", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)
        list_to_create = []
        for row in csv_reader:
            try:
                uea = UsuarioEtiquetaArtista(usuario=Usuario.objects.get(idUsuario=row[0]),
                                             artista=Artista.objects.get(idArtista=row[1]),
                                             tag=Etiqueta.objects.get(idTag=row[2]),
                                             fecha=dt.date(int(row[5]), int(row[4]), int(row[3])))
                list_to_create.append(uea)
            except:
                pass

    UsuarioEtiquetaArtista.objects.bulk_create(list_to_create)
    print("User_TaggedArtists populated")
    
def artist_profile():
    artists = Artista.objects.all()

    for a in artists:
        etiquetas = Etiqueta.objects.filter(usuarioetiquetaartista__artista__idArtista=a.idArtista)
        tag_list = list(etiquetas)
        common_tags = [i[0] for i in Counter(tag_list).most_common(6)]
        a.etiquetas_freq.add(*common_tags)
        
    print("Artist_profile ")

def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})

def form_a(request):
    context = {}
    if request.method == 'POST':
        form = user_id_form(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['userId']
            try:
                list = []
                arts = Artista.objects.filter(usuario__idUsuario=user_id)

                for a in arts:
                    item = []
                    time = UsuarioArtista.objects.filter(usuario_id=user_id, artista_id=a.idArtista).first().tiempoEscucha
                    item.append(a)
                    item.append(time)
                    list.append(item)
            except:
                pass

            context.__setitem__('artists', list)
    else:
        form = user_id_form()

    context.__setitem__('form', form)

    return render(request, 'recomendation/form_a.html', context)


def top_artist(request):
    artists = Artista.objects.annotate(time=Sum('usuarioartista__tiempoEscucha')).order_by('-time')[:3]
    return render(request, 'top_artist.html', {'artists': artists})


def recom(request):
    context = {}
    if request.method == 'POST':
        form = user_id_form(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['userId']
            list = get_related_artists(user_id)

            context.__setitem__('artists', list)
    else:
        form = user_id_form()

    context.__setitem__('form', form)

    return render(request, 'recom.html', context)

#returns a list of list [artist, tags in common], the top ten most related
def get_related_artists(user_id):
    my_tags = user_tags(user_id)
    print(my_tags)
    related_artist = []
    for a in non_listened_artists(user_id):
        relation = 0
        for t in a.etiquetas_freq.all():
            print(t)
            if t in my_tags:
                relation += 1
        related_artist.append([a, relation])

    return Sort(related_artist)[:10]



def non_listened_artists(user_id):

    uas = UsuarioArtista.objects.filter(usuario_id=user_id)
    listened_ids = []
    for ua in uas:
        listened_ids.append(ua.artista.idArtista)

    return list(Artista.objects.exclude(idArtista__in=listened_ids))

def user_tags(user_id):
    # 6 most listened artist by uder
    list_aux = []
    arts = Artista.objects.filter(usuario__idUsuario=user_id)

    for a in arts:
        item = []
        time = UsuarioArtista.objects.filter(usuario_id=user_id, artista_id=a.idArtista).first().tiempoEscucha
        item.append(a)
        item.append(time)
        list_aux.append(item)

    my_6_artists = [i[0] for i in Sort(list_aux)[:6]]

    tags = []
    # iterate over 6 artists, taking its most representatives tags appending to a list
    for a in my_6_artists:
        etiquetas = Etiqueta.objects.filter(artista__idArtista=a.idArtista)
        tag_list = list(etiquetas)
        tags.append(tag_list)

    # Flat the list of tags lists
    merged = list(itertools.chain.from_iterable(tags))
    res = [i[0] for i in Counter(merged).most_common(10)]
    # Taken the top 10 tags
    return res


def Sort(sub_li):
    sub_li.sort(key=lambda x: x[1], reverse=True)
    return sub_li