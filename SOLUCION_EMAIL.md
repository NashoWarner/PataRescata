# Solución para el Error SMTPAuthenticationError en PataRescata

## Problema
Tu aplicación Django está fallando con el error:
```
SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted')
```

## Causa
Gmail requiere configuración especial para aplicaciones de terceros. Las credenciales normales no funcionan.

## Solución Paso a Paso

### 1. Configurar Gmail
1. **Ve a tu cuenta de Gmail**
2. **Activa la verificación en dos pasos** (obligatorio)
   - Gmail → Configuración → Cuentas e importación → Seguridad
   - Activa "Verificación en dos pasos"
3. **Genera una contraseña de aplicación**
   - Gmail → Configuración → Cuentas e importación → Seguridad
   - "Contraseñas de aplicación" → "Otra (nombre personalizado)"
   - Nombre: "Django PataRescata"
   - Copia la contraseña generada (16 caracteres)

### 2. Actualizar settings.py
Reemplaza tu configuración actual con:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'pata.rescata1@gmail.com'
EMAIL_HOST_PASSWORD = 'TU_NUEVA_CONTRASEÑA_DE_APLICACION'
EMAIL_TIMEOUT = 20
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### 3. Probar la Configuración
1. **Reinicia tu servidor Django**
2. **Ve a:** `http://127.0.0.1:8000/probar-email/`
3. **Si funciona:** Verás "Email enviado exitosamente!"
4. **Si falla:** Verás el error específico

### 4. Alternativas para Desarrollo

#### Opción A: Backend de Consola
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
- Los emails se muestran en la consola del servidor
- No se envían realmente
- Perfecto para desarrollo

#### Opción B: Backend de Archivo
```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'emails/'
```
- Los emails se guardan como archivos
- Útil para debugging

## Verificación
1. ✅ Usuario se registra sin errores
2. ✅ Se redirige a `home_perfil` o `mi_login`
3. ✅ Email de verificación se envía (o se maneja el error graciosamente)
4. ✅ Mensajes informativos se muestran al usuario

## Troubleshooting

### Error: "Invalid credentials"
- Verifica que usaste la contraseña de aplicación, no tu contraseña normal
- Asegúrate de que la verificación en dos pasos esté activada

### Error: "Less secure app access"
- Gmail ya no soporta "acceso de aplicaciones menos seguras"
- **Siempre** usa contraseñas de aplicación

### Error: "Connection timeout"
- Verifica tu conexión a internet
- Gmail puede estar bloqueado por firewall corporativo

## Archivos Modificados
- `patarescata/settings.py` - Configuración de email
- `apppatarescata/views.py` - Manejo de errores en registro
- `patarescata/urls.py` - URL para probar email
- `patarescata/email_settings.py` - Configuraciones alternativas
- `SOLUCION_EMAIL.md` - Este archivo

## Próximos Pasos
1. Configura Gmail con contraseña de aplicación
2. Actualiza `settings.py`
3. Prueba con `/probar-email/`
4. Registra un usuario de prueba
5. Verifica que funcione correctamente

## Contacto
Si sigues teniendo problemas, verifica:
- Los logs del servidor Django
- La configuración de Gmail
- Que la contraseña de aplicación sea correcta



