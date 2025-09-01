
# Estructura de Archivos - PataRescata

## Manejo profesional de archivos estáticos y media en Django

### ¿Qué es un archivo estático?
Son archivos que no cambian en tiempo de ejecución: imágenes por defecto, CSS, JS, logos, recursos del proyecto. Se sirven desde la carpeta `static/` y se referencian en los templates con `{% static %}`.

### ¿Qué es un archivo media?
Son archivos subidos por los usuarios (fotos de mascotas, productos, perfiles, etc). Se guardan en la carpeta `media/` y se accede a ellos con la propiedad `.url` del campo File/Image en los modelos.

---


#### 📁 `static/media/` - Recursos Estáticos del Proyecto
Imágenes por defecto, recursos gráficos, imágenes de productos que no cambian y que se usan como referencia o diseño.

```
static/media/
├── imagenes_perfil/          # Imágenes de perfil por defecto
├── imagenes_mascotas/        # Imágenes de mascotas por defecto  
├── productos/                # Imágenes de productos por defecto
└── blog/                     # Imágenes de artículos del blog por defecto
```


#### 📁 `media/` - Archivos subidos por usuarios
Aquí se guardan las imágenes y archivos que los usuarios suben mediante formularios (fotos de mascotas, productos personalizados, imágenes de perfil, etc).
Los modelos Django deben tener el campo `upload_to` configurado para guardar aquí los archivos subidos.
Ejemplo:
```python
imagen = models.ImageField(upload_to='imagenes_mascotas/', blank=True, null=True)
```


#### 📁 `static/images/` - Imágenes del diseño
Imágenes de la interfaz, logos, fondos, iconos, etc. No cambian y se usan solo para el diseño visual.
Incluye `default-pet.jpg` para mostrar cuando no hay imagen subida por el usuario.


### Cambios realizados

1. ✅ Todos los recursos estáticos están en `static/media/` y `static/images/`
2. ✅ Los archivos subidos por usuarios van a `media/`
3. ✅ Los templates usan `{% static %}` para recursos estáticos y `.url` para archivos media
4. ✅ Imagen por defecto en `static/images/default-pet.jpg`
5. ✅ Estructura clara y profesional


### Beneficios

- Separación clara entre recursos estáticos y archivos subidos
- Mejor rendimiento y organización
- Mantenimiento y escalabilidad
- Buenas prácticas Django


### Notas importantes

- Las configuraciones de `MEDIA_URL` y `MEDIA_ROOT` en `settings.py` deben estar correctas para servir archivos subidos
- Los modelos deben usar `upload_to` para guardar en `media/`
- Los templates usan `{% static '...' %}` para recursos estáticos y `{{ objeto.imagen.url }}` para archivos subidos


### Estructura final recomendada

```
PataRescata/
├── static/
│   ├── css/                  # Estilos CSS
│   ├── images/               # Imágenes
├── media/                    # Uploads de usuarios
└── templates/                # Templates HTML
```


### Verificación

- ✅ Carpeta `media/` lista para uploads
- ✅ Imágenes estáticas en `static/media/` y diseño en `static/images/`
- ✅ Templates usan `{% static %}` y `.url` correctamente
- ✅ Imagen por defecto en `static/images/default-pet.jpg`
- ✅ Estructura profesional y mantenible
