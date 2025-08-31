# Estructura de Archivos - PataRescata

## Reorganización de Archivos Estáticos y Media

### Antes de la Reorganización
- Todas las imágenes (estáticas y uploads) estaban en la carpeta `media/`
- No había separación clara entre recursos estáticos y archivos subidos por usuarios

### Después de la Reorganización

#### 📁 `static/media/` - Recursos Estáticos del Proyecto
```
static/media/
├── imagenes_perfil/          # Imágenes de perfil por defecto
├── imagenes_mascotas/        # Imágenes de mascotas por defecto  
├── productos/                # Imágenes de productos por defecto
└── blog/                     # Imágenes de artículos del blog por defecto
```

#### 📁 `media/` - Archivos Subidos por Usuarios
- **Vacía actualmente** - Solo contendrá archivos subidos a través de formularios
- Los modelos Django siguen configurados para usar `upload_to='imagenes_mascotas/'`, etc.

#### 📁 `static/images/` - Imágenes del Diseño
- Logo, fondos, iconos y otras imágenes del diseño de la interfaz
- Incluye `default-pet.jpg` para mascotas sin imagen

### Cambios Realizados

1. ✅ **Movidas todas las carpetas de imágenes estáticas** de `media/` a `static/media/`
2. ✅ **Mantenida la estructura de carpetas** para facilitar futuras referencias
3. ✅ **Verificado que todos los templates** tengan `{% load static %}`
4. ✅ **Creada imagen por defecto** `default-pet.jpg` en `static/images/`
5. ✅ **Carpeta `media/` vacía** lista para recibir uploads de usuarios

### Beneficios de la Reorganización

- **Separación clara** entre recursos estáticos y contenido dinámico
- **Mejor rendimiento** al servir archivos estáticos desde `static/`
- **Mantenimiento más fácil** de recursos del proyecto
- **Escalabilidad** para futuras implementaciones
- **Buenas prácticas** de Django para manejo de archivos

### Notas Importantes

- **No se modificaron** las configuraciones de `MEDIA_URL` y `MEDIA_ROOT` en `settings.py`
- **Los modelos Django** siguen funcionando igual para uploads de usuarios
- **Todas las rutas en templates** ya usan `{% static %}` correctamente
- **La aplicación seguirá funcionando** sin cambios en el código

### Estructura Final Recomendada

```
PataRescata/
├── static/
│   ├── css/                  # Estilos CSS
│   ├── images/               # Imágenes del diseño
│   └── media/                # Recursos estáticos del proyecto
│       ├── imagenes_perfil/
│       ├── imagenes_mascotas/
│       ├── productos/
│       └── blog/
├── media/                    # Uploads de usuarios (vacía actualmente)
└── templates/                # Templates HTML
```

### Verificación

- ✅ Carpeta `media/` vacía
- ✅ Todas las imágenes estáticas en `static/media/`
- ✅ Todos los templates con `{% load static %}`
- ✅ Imagen por defecto creada en `static/images/default-pet.jpg`
- ✅ Estructura de carpetas mantenida
