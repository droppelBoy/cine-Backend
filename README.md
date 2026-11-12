# CineStar - Backend

## Descripción del proyecto

CineStar es un sistema de gestión de cine desarrollado como parte de la segunda evaluación de Desarrollo de Aplicaciones Web.

Este proyecto corresponde al Back-End de la aplicación realizada anteriormente en React. Su objetivo es administrar películas, salas, funciones y reservas mediante una API REST conectada a una base de datos.

El sistema permite registrar información, consultar funciones y controlar la disponibilidad de asientos.

## Tecnologías utilizadas

- Python
- Django
- Django REST Framework
- SQLite
- Git y GitHub

## Modelos de datos

### Pelicula
Almacena la información de las películas:
- Título
- Género
- Duración
- Clasificación
- Precio
- Director
- Sinopsis
- Imagen

### Sala
Representa las salas del cine:
- Nombre
- Capacidad

### Funcion
Registra las funciones disponibles:
- Película
- Sala
- Fecha
- Horario
- Asientos disponibles

Se relaciona con Pelicula y Sala mediante ForeignKey.

### Reserva
Almacena las reservas realizadas:
- Función
- Nombre del cliente
- Correo electrónico
- Cantidad de asientos
- Asientos seleccionados
- Total pagado
- Fecha de reserva

Se relaciona con Funcion mediante ForeignKey.

## Funcionalidades del Back-End

- Gestión de películas, salas y funciones.
- Operaciones CRUD mediante API REST.
- Registro y consulta de reservas.
- Validación de cantidades y asientos seleccionados.
- Verificación de disponibilidad antes de registrar reservas.
- Descuento de asientos disponibles al crear una reserva.
- Almacenamiento de información mediante Django ORM y SQLite.

## Instalación del proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/droppelBoy/cine-Backend.git
cd cine-Backend
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
```

Activar el entorno virtual en Windows:

```bash
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear y aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Ejecutar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en:

http://127.0.0.1:8000/

## API REST

Las rutas principales del proyecto son:

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/peliculas/ | Listar películas |
| POST | /api/peliculas/ | Crear película |
| GET | /api/peliculas/1/ | Consultar película |
| PUT | /api/peliculas/1/ | Actualizar película |
| DELETE | /api/peliculas/1/ | Eliminar película |
| GET | /api/salas/ | Listar salas |
| POST | /api/salas/ | Crear sala |
| GET | /api/funciones/ | Listar funciones |
| POST | /api/funciones/ | Crear función |
| GET | /api/reservas/ | Consultar reservas |
| POST | /api/reservas/ | Registrar reserva |

Las rutas de detalle utilizan el identificador del registro correspondiente.

## Pruebas

El proyecto incluye pruebas automatizadas en cinema/tests.py.

Para ejecutarlas:

```bash
python manage.py test cinema
```

Las pruebas contemplan creación de reservas, validación de asientos, disponibilidad y respuestas HTTP.

Los resultados deben verificarse ejecutando el proyecto en un entorno local.

## Estructura del proyecto

```text
cine-Backend/
├── cinema/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core/
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

## Integración futura

La API REST está diseñada para permitir una futura conexión con el Front-End desarrollado en React.

Esta integración no es obligatoria para la segunda evaluación.
