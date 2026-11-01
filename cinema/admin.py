from django.contrib import admin
from .models import Pelicula, Sala, Funcion, Reserva

@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'genero', 'duracion', 'clasificacion', 'precio')
    search_fields = ('titulo', 'genero')

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad')

@admin.register(Funcion)
class FuncionAdmin(admin.ModelAdmin):
    list_display = ('pelicula', 'sala', 'fecha', 'horario', 'asientos_disponibles')
    list_filter = ('fecha', 'sala')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'funcion', 'cantidad_asientos', 'total_pagado', 'fecha_reserva')
    search_fields = ('nombre_cliente', 'email_cliente')