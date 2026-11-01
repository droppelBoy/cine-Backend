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