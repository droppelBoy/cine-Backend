from django.db import models
from django.core.validators import MinValueValidator

class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    genero = models.CharField(max_length=100)
    duracion = models.CharField(max_length=50)
    clasificacion = models.CharField(max_length=20, default='TE+7')
    precio = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    director = models.CharField(max_length=100, default='Droppel')
    sinopsis = models.TextField()
    imagen = models.CharField(max_length=500)

    def __str__(self):
        return self.titulo

class Sala(models.Model):
    nombre = models.CharField(max_length=50)
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} (Capacidad: {self.capacidad})"

class Funcion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='funciones')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='funciones')
    fecha = models.DateField()
    horario = models.TimeField()
    asientos_disponibles = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.pk and self.asientos_disponibles is None:
            self.asientos_disponibles = self.sala.capacidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pelicula.titulo} - {self.fecha} {self.horario}"

class Reserva(models.Model):
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE, related_name='reservas')
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    cantidad_asientos = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    asientos_seleccionados = models.CharField(max_length=255)
    total_pagado = models.PositiveIntegerField()
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.nombre_cliente} para {self.funcion.pelicula.titulo}"