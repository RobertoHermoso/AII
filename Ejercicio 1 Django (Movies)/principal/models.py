#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from enum import Enum


class categoria(Enum):   # A subclass of Enum
    UN = "unknown"
    AC = "action"
    AD = "adventure"
    AN = "anomiation"
    CH = 'children`s'
    CO = 'comedy'
    CR = 'crime'
    DO = 'documental'
    DR = 'drama'
    FA = 'fantasy'
    FN = 'fil-noir'
    HO = 'horror'
    MU = 'musica'
    MY = 'mystery'
    RO = 'romance'
    SF = 'sci-fi'
    TH = 'thriller'
    WA = 'war'
    WE = 'western'

    @classmethod
    def all(self):
        return [categoria.UN, categoria.AC, categoria.AD, categoria.AN, categoria.CH, categoria.CO, categoria.CR,
                categoria.DO, categoria.DR, categoria.FA, categoria.FN, categoria.HO, categoria.MU, categoria.MY,
                categoria.RO, categoria.SF, categoria.TH, categoria.WA, categoria.WE]


class Usuario(models.Model):
    nombre = models.TextField(help_text='Nombre')
    apellidos = models.TextField(help_text='Apellidos')
    fecha_de_nacimiento = models.DateField
    categoria_preferida = models.CharField(max_length=15, choices=[(tag.name, tag.value) for tag in categoria.all()])

    def __str__(self):
        return self.nombre + " " + self.apellidos


class Director(models.Model):
    nombre = models.TextField(help_text='Nombre')
    apellidos = models.TextField(help_text='Apellidos')
    biografia = models.TextField(help_text='Biografía')

    def __str__(self):
        return self.nombre + " " + self.apellidos


class Pelicula(models.Model):
    titulo = models.TextField(help_text='Titulo')
    director = models.ForeignKey(Director,on_delete=models.CASCADE)
    resumen = models.TextField(help_text='Resumen de la pelicula')
    categoria = models.CharField(max_length=15, choices=[(tag.name, tag.value) for tag in categoria.all()])

    def __str__(self):
        return self.titulo


