#encoding:utf-8

from django.db import models


class Etiqueta(models.Model):

    tagValue = models.TextField(max_length=100)
    idTag = models.IntegerField(primary_key=True)


class Artista(models.Model):

    #  Fields
    url = models.URLField()
    pictureUrl = models.URLField()
    nombre = models.TextField(max_length=100)
    idArtista = models.IntegerField(primary_key=True)
    etiquetas_freq = models.ManyToManyField(Etiqueta)



class UsuarioEtiquetaArtista(models.Model):

    #  Relationships
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    tag = models.ForeignKey("Etiqueta", on_delete=models.CASCADE)
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)

    #  Fields
    fecha = models.DateField()
    idUsuarioEtiquetaArtista = models.IntegerField(primary_key=True)


class Usuario(models.Model):

    #  Fields
    idUsuario = models.IntegerField(primary_key=True)
    artista = models.ManyToManyField(Artista, through='UsuarioArtista')


class UsuarioArtista(models.Model):

    #  Relationships
    artista = models.ForeignKey("Artista", on_delete=models.CASCADE)
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)

    #  Fields
    tiempoEscucha = models.IntegerField()
    idUsuarioArtista = models.IntegerField(primary_key=True)

