# CineStar - Documentación de API REST

## 1. Descripción

La API REST de CineStar fue desarrollada utilizando Python, Django y Django REST Framework.

Permite gestionar películas, salas, funciones y reservas mediante operaciones CRUD, almacenando la información en SQLite.

URL base local: http://127.0.0.1:8000/api/

Los endpoints utilizan JSON para enviar y recibir información.

## 2. Métodos HTTP

| Método | Descripción |
|--------|-------------|
| GET | Consultar registros |
| POST | Crear registros |
| PUT | Actualizar un registro completo |
| PATCH | Actualizar parcialmente un registro |
| DELETE | Eliminar registros |

## 3. Endpoints de películas

| Método | Ruta | Funcionalidad |
|--------|------|---------------|
| GET | /api/peliculas/ | Listar películas |
| GET | /api/peliculas/1/ | Consultar una película |
| POST | /api/peliculas/ | Crear una película |
| PUT | /api/peliculas/1/ | Actualizar una película |
| PATCH | /api/peliculas/1/ | Actualización parcial |
| DELETE | /api/peliculas/1/ | Eliminar una película |

### Ejemplo POST /api/peliculas/

```json
{
  "titulo": "Interstellar",
  "genero": "Ciencia ficcion",
  "duracion": "169 min",
  "clasificacion": "TE+7",
  "precio": 5000,
  "director": "Christopher Nolan",
  "sinopsis": "Un grupo de astronautas viaja por el espacio.",
  "imagen": "interstellar.jpg"
}
```

## 4. Endpoints de salas

| Método | Ruta | Funcionalidad |
|--------|------|---------------|
| GET | /api/salas/ | Listar salas |
| GET | /api/salas/1/ | Consultar una sala |
| POST | /api/salas/ | Crear una sala |
| PUT | /api/salas/1/ | Actualizar una sala |
| PATCH | /api/salas/1/ | Actualizar parcialmente |
| DELETE | /api/salas/1/ | Eliminar una sala |

### Ejemplo POST /api/salas/

```json
{
  "nombre": "Sala 1",
  "capacidad": 20
}
```

## 5. Endpoints de funciones

| Método | Ruta | Funcionalidad |
|--------|------|---------------|
| GET | /api/funciones/ | Listar funciones |
| GET | /api/funciones/1/ | Consultar una función |
| POST | /api/funciones/ | Crear una función |
| PUT | /api/funciones/1/ | Actualizar una función |
| PATCH | /api/funciones/1/ | Actualizar parcialmente |
| DELETE | /api/funciones/1/ | Eliminar una función |

### Ejemplo POST /api/funciones/

```json
{
  "pelicula": 1,
  "sala": 1,
  "fecha": "2026-11-20",
  "horario": "18:30:00",
  "asientos_disponibles": 20
}
```

Los campos pelicula y sala corresponden a identificadores de registros existentes.

## 6. Endpoints de reservas

| Método | Ruta | Funcionalidad |
|--------|------|---------------|
| GET | /api/reservas/ | Listar reservas |
| GET | /api/reservas/1/ | Consultar una reserva |
| POST | /api/reservas/ | Crear una reserva |
| PUT | /api/reservas/1/ | Actualizar una reserva |
| PATCH | /api/reservas/1/ | Actualizar parcialmente |
| DELETE | /api/reservas/1/ | Eliminar una reserva |

### Ejemplo POST /api/reservas/

```json
{
  "funcion": 1,
  "nombre_cliente": "Cliente Prueba",
  "email_cliente": "cliente@ejemplo.com",
  "cantidad_asientos": 2,
  "asientos_seleccionados": "A1,A2",
  "total_pagado": 10000
}
```

La función debe existir previamente.

## 7. Validaciones de reservas

El sistema incorpora validaciones para:

- Evitar cantidades de asientos menores a 1.
- Comprobar que la cantidad coincida con los asientos seleccionados.
- Impedir asientos repetidos en una misma reserva.
- Detectar asientos registrados en otras reservas de la función.
- Verificar que existan suficientes asientos disponibles.

Al crear una reserva válida, se descuentan los asientos solicitados de la disponibilidad de la función.

Estas validaciones deben comprobarse mediante pruebas de ejecución.

## 8. Códigos de respuesta HTTP

| Código | Significado |
|--------|-------------|
| 200 OK | Consulta o actualización exitosa |
| 201 Created | Registro creado correctamente |
| 204 No Content | Registro eliminado |
| 400 Bad Request | Datos inválidos |
| 404 Not Found | Registro inexistente |

## 9. Pruebas de funcionamiento

Los endpoints pueden probarse mediante Postman, Insomnia o la interfaz navegable de Django REST Framework.

Para ejecutar las pruebas automatizadas:

```bash
python manage.py test cinema
```

El proyecto incluye pruebas en cinema/tests.py.

Las pruebas deben ejecutarse para confirmar su resultado y obtener evidencias de funcionamiento.

## 10. Consideraciones

- Los identificadores utilizados en los ejemplos son referenciales.
- Los datos se almacenan mediante Django ORM y SQLite.
- No se requiere autenticación para esta evaluación.
- La conexión con React queda pendiente para una etapa posterior.
- La actualización y eliminación de reservas requieren verificar el ajuste de disponibilidad.
```
