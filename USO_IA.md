Proyecto: CineStar – Back-End

**Herramienta utilizada:** ChatGPT (OpenAI)

Durante el desarrollo del Back-End de CineStar utilizamos ChatGPT como herramienta de apoyo para comprender conceptos, desarrollar funcionalidades, solucionar errores y comprobar el funcionamiento de nuestra API REST.

## Uso estimado de inteligencia artificial

| Archivo | Uso estimado de IA | Descripción |
|---|---|---|
| models.py | 20% | Orientación sobre modelos y relaciones entre entidades. |
| serializers.py | 70% | Apoyo en la implementación y corrección de validaciones de reservas, asientos y disponibilidad. |
| views.py | 65% | Apoyo en los ViewSets y la sincronización de asientos al crear, modificar y eliminar reservas. |
| urls.py | 15% | Orientación para configurar rutas de la API REST. |
| settings.py | 15% | Apoyo en la configuración de Django y sus dependencias. |
| README.md | 20% | Orientación para revisar la documentación del proyecto. |

Los porcentajes son estimaciones aproximadas de participación de IA y deben ajustarse según el trabajo real de los integrantes.

## Preguntas de reflexión

### 1. ¿En qué aspectos utilizamos inteligencia artificial?

Utilizamos ChatGPT para resolver errores de Python y Django, comprender el funcionamiento de serializers y ViewSets, implementar validaciones y comprobar las operaciones CRUD de nuestra API.

### 2. ¿Qué partes desarrollamos principalmente nosotros?

Trabajamos en la configuración y ejecución local del proyecto, el registro de películas, salas, funciones y reservas, las pruebas en Django REST Framework y la gestión del repositorio GitHub.

### 3. ¿Qué problemas encontramos en las respuestas de la IA?

Encontramos errores de indentación y problemas relacionados con la actualización de asientos disponibles. Algunas propuestas necesitaron modificaciones y nuevas pruebas antes de funcionar correctamente.

### 4. ¿Cómo verificamos el código sugerido?

Ejecutamos `python manage.py check`, iniciamos el servidor Django, consultamos los endpoints y probamos operaciones de creación, modificación y eliminación de registros. También comprobamos que el sistema rechazara asientos ocupados.

### 5. ¿Qué conocimientos adquirimos?

Aprendimos a trabajar con modelos, relaciones entre tablas, serializers, ViewSets, operaciones CRUD, validaciones, persistencia de datos con SQLite y control de versiones mediante Git y GitHub.

## Conclusión

La inteligencia artificial fue una herramienta de apoyo durante el desarrollo. Las propuestas se revisaron, adaptaron y probaron en el proyecto para comprender su funcionamiento y corregir los problemas encontrados.
:::