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
        funcion = data.get('funcion', getattr(self.instance, 'funcion', None))
        cantidad = data.get('cantidad_asientos', getattr(self.instance, 'cantidad_asientos', None))
        asientos = data.get('asientos_seleccionados', getattr(self.instance, 'asientos_seleccionados', ''))

        if not funcion or cantidad is None:
            return data

        if cantidad < 1:
            raise serializers.ValidationError(
                "Debes reservar al menos un asiento."
            )

        lista_asientos = [
            asiento.strip().upper()
            for asiento in asientos.split(',')
            if asiento.strip()
        ]

        if len(lista_asientos) != cantidad:
            raise serializers.ValidationError(
                "La cantidad de asientos no coincide con los seleccionados."
            )

        if len(lista_asientos) != len(set(lista_asientos)):
            raise serializers.ValidationError(
                "No puedes seleccionar el mismo asiento dos veces."
            )

        reservas = Reserva.objects.filter(funcion=funcion)
        if self.instance:
            reservas = reservas.exclude(pk=self.instance.pk)

        ocupados = set()
        for reserva in reservas:
            ocupados.update(
                asiento.strip().upper()
                for asiento in reserva.asientos_seleccionados.split(',')
            )

        if ocupados.intersection(lista_asientos):
            raise serializers.ValidationError(
                "Uno o más asientos seleccionados ya están reservados."
            )

        if self.instance is None and cantidad > funcion.asientos_disponibles:
            raise serializers.ValidationError(
                f"Solo quedan {funcion.asientos_disponibles} asientos disponibles."
            )

        return data

    def create(self, validated_data):
        funcion = validated_data['funcion']
        cantidad = validated_data['cantidad_asientos']
        # Descontar asientos al confirmar la reserva
        funcion.asientos_disponibles -= cantidad
        funcion.save()
        return super().create(validated_data)
