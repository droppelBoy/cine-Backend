from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PeliculaViewSet, SalaViewSet, FuncionViewSet, ReservaViewSet

router = DefaultRouter()
router.register(r'peliculas', PeliculaViewSet)
router.register(r'salas', SalaViewSet)
router.register(r'funciones', FuncionViewSet)
router.register(r'reservas', ReservaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]