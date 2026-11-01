from rest_framework import serializers
from .models import Pelicula, Sala, Funcion, Reserva

class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = '__all__'

    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'

class FuncionSerializer(serializers.ModelSerializer):
    pelicula_titulo = serializers.ReadOnlyField(source='pelicula.titulo')
    sala_nombre = serializers.ReadOnlyField(source='sala.nombre')

    class Meta:
        model = Funcion
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

    def validate(self, data):
        funcion = data.get('funcion')
        cantidad = data.get('cantidad_asientos')
        if funcion and cantidad:
            if cantidad > funcion.asientos_disponibles:
                raise serializers.ValidationError(
                    f"No hay suficientes asientos disponibles. Quedan solo {funcion.asientos_disponibles}."
                )
        return data

    def create(self, validated_data):
        funcion = validated_data['funcion']
        cantidad = validated_data['cantidad_asientos']
        # Descontar asientos al confirmar la reserva
        funcion.asientos_disponibles -= cantidad
        funcion.save()
        return super().create(validated_data)