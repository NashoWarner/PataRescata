# Configuraciones alternativas de email para Gmail
# Copia la configuración que prefieras a tu settings.py

# Opción 1: TLS (Recomendada)
EMAIL_CONFIG_TLS = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': 'smtp.gmail.com',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
    'EMAIL_USE_SSL': False,
    'EMAIL_HOST_USER': 'tu-email@gmail.com',
    'EMAIL_HOST_PASSWORD': 'tu-contraseña-de-aplicacion',
    'EMAIL_TIMEOUT': 20,
    'DEFAULT_FROM_EMAIL': 'tu-email@gmail.com',
}

# Opción 2: SSL (Alternativa)
EMAIL_CONFIG_SSL = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': 'smtp.gmail.com',
    'EMAIL_PORT': 465,
    'EMAIL_USE_TLS': False,
    'EMAIL_USE_SSL': True,
    'EMAIL_HOST_USER': 'tu-email@gmail.com',
    'EMAIL_HOST_PASSWORD': 'tu-contraseña-de-aplicacion',
    'EMAIL_TIMEOUT': 20,
    'DEFAULT_FROM_EMAIL': 'tu-email@gmail.com',
}

# Opción 3: Backend de consola para desarrollo (No envía emails reales)
EMAIL_CONFIG_CONSOLE = {
    'EMAIL_BACKEND': 'django.core.mail.backends.console.EmailBackend',
}

# Opción 4: Backend de archivo para desarrollo (Guarda emails en archivos)
EMAIL_CONFIG_FILE = {
    'EMAIL_BACKEND': 'django.core.mail.backends.filebased.EmailBackend',
    'EMAIL_FILE_PATH': 'emails/',  # Crear esta carpeta en tu proyecto
}



