from django.test import TestCase
from datetime import date, time, timedelta
from rest_framework.test import APIClient
from .models import Pelicula, Sala, Funcion, Reserva


class ReservaAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.pelicula = Pelicula.objects.create(
            titulo="Interstellar",
            genero="Ciencia ficcion",
            duracion="169 min",
            clasificacion="TE+7",
            precio=5000,
            director="Christopher Nolan",
            sinopsis="Viaje espacial",
            imagen="interstellar.jpg"
        )

        self.sala = Sala.objects.create(
            nombre="Sala 1",
            capacidad=20
        )

        self.funcion = Funcion.objects.create(
            pelicula=self.pelicula,
            sala=self.sala,
            fecha=date.today() + timedelta(days=1),
            horario=time(18, 30),
            asientos_disponibles=20
        )

    def datos_reserva(self, asientos="A1,A2", cantidad=2):
        return {
            "funcion": self.funcion.id,
            "nombre_cliente": "Cliente Prueba",
            "email_cliente": "cliente@ejemplo.com",
            "cantidad_asientos": cantidad,
            "asientos_seleccionados": asientos,
            "total_pagado": 10000
        }

    def test_listar_peliculas(self):
        respuesta = self.client.get("/api/peliculas/")
        self.assertEqual(respuesta.status_code, 200)

    def test_crear_reserva(self):
        respuesta = self.client.post(
            "/api/reservas/",
            self.datos_reserva(),
            format="json"
        )
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Reserva.objects.count(), 1)

        self.funcion.refresh_from_db()
        self.assertEqual(self.funcion.asientos_disponibles, 18)

    def test_asientos_repetidos(self):
        respuesta = self.client.post(
            "/api/reservas/",
            self.datos_reserva("A1,A1"),
            format="json"
        )
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Reserva.objects.count(), 0)

    def test_asientos_ya_reservados(self):
        self.client.post(
            "/api/reservas/",
            self.datos_reserva("A1,A2"),
            format="json"
        )

        respuesta = self.client.post(
            "/api/reservas/",
            self.datos_reserva("A2,A3"),
            format="json"
        )
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Reserva.objects.count(), 1)

    def test_cantidad_incorrecta(self):
        respuesta = self.client.post(
            "/api/reservas/",
            self.datos_reserva("A1,A2", 3),
            format="json"
        )
        self.assertEqual(respuesta.status_code, 400)

    def test_reserva_supera_disponibilidad(self):
        respuesta = self.client.post(
            "/api/reservas/",
            self.datos_reserva("A1,A2,A3", 21),
            format="json"
        )
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Reserva.objects.count(), 0)

    def test_eliminar_reserva(self):
        respuesta = self.client.post(
            "/api/reservas/",
            self.datos_reserva(),
            format="json"
        )
        self.assertEqual(respuesta.status_code, 201)

        reserva_id = respuesta.data["id"]

        respuesta = self.client.delete(
            f"/api/reservas/{reserva_id}/"
        )
        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(Reserva.objects.count(), 0)
