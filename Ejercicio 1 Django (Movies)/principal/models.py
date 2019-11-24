#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    nombre = models.TextField(help_text='Nombre')
    apellidos = models.TextField(help_text='Apellidos')
    fecha_de_nacimiento = models.TextField(help_text='Fecha de nacimiento')
    categoria_preferida = models.TextField(help_text='Tu categoría preferida')

    def __str__(self):
        return self.nombre + " " + self.apellidos


class Director(models.Model):
    nombre = models.TextField(help_text='Nombre')
    apellidos = models.TextField(help_text='Apellidos')
    biografia = models.TextField(help_text='Biografía')

    def __str__(self):
        return self.nombre + " " + self.apellidos


class Pelicula(models.Model):
    titulo = models.TextField(help_text='Nombre')
    aapellidos = models.TextField(help_text='Apellidos')
    director = models.ForeignKey(Director,on_delete=models.CASCADE)
    resumen = models.TextField(help_text='Resumen de la pelicula')
    categoria = models.TextField(help_text='Tu categoría preferida')

    def __str__(self):
        return self.titulo


