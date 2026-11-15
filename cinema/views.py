
from django.db import transaction
from django.db.models import Sum
from rest_framework import viewsets

from .models import Pelicula, Sala, Funcion, Reserva

from .serializers import (
    PeliculaSerializer,
    SalaSerializer,
    FuncionSerializer,
    ReservaSerializer
)

class PeliculaViewSet(viewsets.ModelViewSet):
    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer

class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

class FuncionViewSet(viewsets.ModelViewSet):
    queryset = Funcion.objects.all()
    serializer_class = FuncionSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def sincronizar_asientos(self, funcion_id):
        funcion = Funcion.objects.select_for_update().select_related(
            'sala'
        ).get(pk=funcion_id)

        total_reservado = Reserva.objects.filter(
            funcion_id=funcion_id
        ).aggregate(
            total=Sum('cantidad_asientos')
        )['total'] or 0

        funcion.asientos_disponibles = max(
            funcion.sala.capacidad - total_reservado,
            0
        )

        funcion.save(update_fields=['asientos_disponibles'])

    def perform_create(self, serializer):
        with transaction.atomic():
            reserva = serializer.save()
            self.sincronizar_asientos(reserva.funcion_id)

    def perform_update(self, serializer):
        with transaction.atomic():
            funcion_anterior_id = self.get_object().funcion_id
            reserva = serializer.save()

            self.sincronizar_asientos(funcion_anterior_id)

            if reserva.funcion_id != funcion_anterior_id:
                self.sincronizar_asientos(reserva.funcion_id)

    def perform_destroy(self, instance):
        with transaction.atomic():
            funcion_id = instance.funcion_id

            instance.delete()

            self.sincronizar_asientos(funcion_id)