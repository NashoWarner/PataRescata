# Modelos de la aplicación Django

Este proyecto Django contiene varios modelos que representan las entidades principales de la aplicación. A continuación, se describen estos modelos:

## Modelo Mascota

Representa una mascota con los siguientes campos:

- `nombre_mascota`: Nombre de la mascota (cadena de hasta 20 caracteres).
- `edad_mascota`: Edad de la mascota (cadena de hasta 5 caracteres).
- `tamaño_mascota`: Tamaño de la mascota (cadena de hasta 50 caracteres).
- `comuna_mascota`: Comuna de la mascota (cadena de hasta 50 caracteres).
- `region`: Región de la mascota (cadena de hasta 50 caracteres).
- `descripcion`: Descripción de la mascota (cadena de hasta 100 caracteres).
- `imagen`: Imagen de la mascota (campo de imagen, opcional).
- `adopcion_solicitada`: Indica si se ha solicitado la adopción de la mascota (booleano, por defecto `False`).

## Modelo FAQ

Representa una entrada de preguntas frecuentes con los siguientes campos:

- `pregunta`: La pregunta (cadena de hasta 1000 caracteres).
- `respuesta`: La respuesta a la pregunta (cadena de hasta 1000 caracteres).

## Modelo Usuario

Representa un usuario con los siguientes campos:

- `email`: Email del usuario (campo de email, debe ser único).
- `nombre`: Nombre del usuario (cadena de hasta 50 caracteres).
- `telefono`: Teléfono del usuario (cadena de hasta 15 caracteres, validado con la función `Numero`).
- `rut_empresa`: RUT de la empresa del usuario (cadena de hasta 20 caracteres, opcional, validado con la función `rut`).
- `email_verificado`: Indica si el email del usuario ha sido verificado (booleano, por defecto `False`).
- `token_verificacion`: Token de verificación del email del usuario (cadena de 40 caracteres, generada con la función `generar_token`).
- `is_active`: Indica si el usuario está activo (booleano, por defecto `True`).
- `is_staff`: Indica si el usuario es miembro del personal (booleano, por defecto `False`).

## Modelo MascotaFundacion

Representa una relación entre una mascota y un usuario (adoptante) con los siguientes campos:

- `mascota`: Referencia a la mascota (clave foránea al modelo `Mascota`).
- `adoptante`: Referencia al usuario adoptante (clave foránea al modelo `Usuario`).

## Modelo Adopcion

Representa una adopción con los siguientes campos:

- `adoptante`: Referencia al usuario adoptante (clave foránea al modelo `Usuario`).
- `mascota`: Referencia a la mascota (clave foránea al modelo `Mascota`).
- `fecha_adopcion`: Fecha en que se solicitó la adopción (campo de fecha, se establece automáticamente al crear la adopción).
- `solicitada`: Indica si la adopción ha sido solicitada (booleano, por defecto `True`).


## Código de la aplicación web Django para un sistema de adopción de mascotas

### Función `faq(request)`

Esta función maneja las solicitudes a la página de preguntas frecuentes (FAQ). Si la solicitud es un POST, intenta guardar una nueva pregunta en la base de datos. Si la solicitud es un GET, simplemente muestra todas las preguntas existentes.

### Función `agregarMascota(request)`

Permite a los usuarios autenticados agregar una nueva mascota al sistema. Si la solicitud es un POST, guarda la nueva mascota en la base de datos. Si la solicitud es un GET, simplemente muestra un formulario para agregar una nueva mascota.

### Funciones `buscar_animales(request)` y `resultado_busqueda(request)`

Estas funciones permiten a los usuarios buscar mascotas en el sistema. Ambas funciones filtran las mascotas en la base de datos según los criterios de búsqueda proporcionados en la solicitud GET.

### Función `registro_usuario(request)`

Maneja el registro de nuevos usuarios. Si la solicitud es un POST, guarda el nuevo usuario en la base de datos y envía un correo electrónico de verificación. Si la solicitud es un GET, simplemente muestra un formulario de registro.

### Funciones `mi_login(request)` y `logout_view(request)`

Estas funciones manejan el inicio y cierre de sesión de los usuarios.

### Funciones `info_perfil(request)` y `actualizar_perfil(request)`

Permiten a los usuarios autenticados ver y actualizar su información de perfil.

### Función `eliminar_cuenta(request)`

Permite a los usuarios autenticados eliminar su cuenta.

### Funciones `realizar_adopcion(request, animal_id)` y `mis_solicitudes(request)`

Estas funciones permiten a los usuarios autenticados solicitar la adopción de una mascota y ver sus solicitudes de adopción existentes.

### Función `verificar_cuenta(request, token)`

Verifica la cuenta de un usuario cuando hacen clic en el enlace de verificación que se les envió por correo electrónico.
