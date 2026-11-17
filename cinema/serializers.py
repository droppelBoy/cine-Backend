
from django.db import transaction
from rest_framework import serializers
from .models import Pelicula, Sala, Funcion, Reserva


class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = '__all__'

    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "El precio no puede ser negativo."
            )
        return value


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'


class FuncionSerializer(serializers.ModelSerializer):
    pelicula_titulo = serializers.ReadOnlyField(
        source='pelicula.titulo'
    )
    sala_nombre = serializers.ReadOnlyField(
        source='sala.nombre'
    )

    class Meta:
        model = Funcion
        fields = '__all__'


class ReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = '__all__'
        read_only_fields = ('total_pagado',)

    def validate(self, data):

        funcion = data.get(
            'funcion',
            getattr(self.instance, 'funcion', None)
        )

        cantidad = data.get(
            'cantidad_asientos',
            getattr(self.instance, 'cantidad_asientos', None)
        )

        asientos = data.get(
            'asientos_seleccionados',
            getattr(self.instance, 'asientos_seleccionados', '')
        )

        if not funcion or cantidad is None:
            return data

        # Validar cantidad mínima
        if cantidad < 1:
            raise serializers.ValidationError(
                "Debes reservar al menos un asiento."
            )

        # Limitar máximo de 4 asientos
        if cantidad > 4:
            raise serializers.ValidationError(
                "No puedes reservar más de 4 asientos."
            )

        # Convertir los asientos en una lista
        lista_asientos = [
            asiento.strip().upper()
            for asiento in (asientos or '').split(',')
            if asiento.strip()
        ]

        # Comprobar que la cantidad coincida
        if len(lista_asientos) != cantidad:
            raise serializers.ValidationError(
                "La cantidad de asientos no coincide con los seleccionados."
            )

        # Evitar asientos repetidos
        if len(lista_asientos) != len(set(lista_asientos)):
            raise serializers.ValidationError(
                "No puedes seleccionar el mismo asiento dos veces."
            )

        # Consultar reservas de la misma función
        reservas = Reserva.objects.filter(funcion=funcion)

        if self.instance:
            reservas = reservas.exclude(pk=self.instance.pk)

        # Obtener los asientos ocupados
        ocupados = set()

        for reserva in reservas:
            ocupados.update(
                asiento.strip().upper()
                for asiento in (reserva.asientos_seleccionados or '').split(',')
                if asiento.strip()
            )

        # Comprobar si algún asiento ya está reservado
        if ocupados.intersection(lista_asientos):
            raise serializers.ValidationError(
                "Uno o más asientos seleccionados ya están reservados."
            )

        # Consultar disponibilidad
        disponibles = funcion.asientos_disponibles

        if self.instance and self.instance.funcion_id == funcion.id:
            disponibles += self.instance.cantidad_asientos

        if cantidad > disponibles:
            raise serializers.ValidationError(
                f"Solo quedan {disponibles} asientos disponibles."
            )

        # CALCULAR AUTOMÁTICAMENTE EL PRECIO
        data['total_pagado'] = (
            cantidad * funcion.pelicula.precio
        )

        return data

    @transaction.atomic
    def create(self, validated_data):

        funcion = Funcion.objects.select_for_update().get(
            pk=validated_data['funcion'].pk
        )

        validated_data['funcion'] = funcion

        self.validate(validated_data)

        cantidad = validated_data['cantidad_asientos']

        reserva = super().create(validated_data)

        funcion.asientos_disponibles -= cantidad
        funcion.save(update_fields=['asientos_disponibles'])

        return reserva

    @transaction.atomic
    def update(self, instance, validated_data):

        funcion_anterior = Funcion.objects.select_for_update().get(
            pk=instance.funcion_id
        )

        funcion_nueva_id = validated_data.get(
            'funcion',
            instance.funcion
        ).pk

        if funcion_nueva_id == funcion_anterior.pk:
            funcion_nueva = funcion_anterior
        else:
            funcion_nueva = Funcion.objects.select_for_update().get(
                pk=funcion_nueva_id
            )

        validated_data['funcion'] = funcion_nueva

        self.validate(validated_data)

        cantidad_anterior = instance.cantidad_asientos

        cantidad_nueva = validated_data.get(
            'cantidad_asientos',
            cantidad_anterior
        )

        reserva = super().update(instance, validated_data)

        funcion_anterior.asientos_disponibles += cantidad_anterior
        funcion_nueva.asientos_disponibles -= cantidad_nueva

        funcion_anterior.save(
            update_fields=['asientos_disponibles']
        )

        if funcion_nueva.pk != funcion_anterior.pk:
            funcion_nueva.save(
                update_fields=['asientos_disponibles']
            )

        return reserva


