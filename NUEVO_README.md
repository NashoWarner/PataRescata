# PataRescata - Plataforma de Adopción de Mascotas

Este documento detalla los cambios realizados en la aplicación PataRescata, las nuevas tecnologías implementadas y cómo inicializar el proyecto desde cero en un nuevo entorno.

## Evolución del Proyecto

PataRescata ha experimentado una transformación significativa, evolucionando desde una aplicación Django tradicional con templates a una arquitectura moderna que separa el backend (Django/DRF) y el frontend (React).

### Principales Cambios Arquitectónicos

#### 1. Separación de Backend y Frontend

- **Antes**: Aplicación monolítica Django con templates HTML.
- **Ahora**: 
  - Backend: API REST con Django REST Framework
  - Frontend: SPA (Single Page Application) con React

#### 2. Dockerización

- **Antes**: Despliegue manual y configuración dependiente del entorno.
- **Ahora**: Aplicación completamente containerizada con Docker, lo que garantiza consistencia entre entornos de desarrollo y producción.

#### 3. Migración a React

- **Antes**: Templates Django con bloques de contenido.
- **Ahora**: Componentes React reutilizables y enrutamiento del lado del cliente.

#### 4. Proxy Inverso

- Se implementó Nginx como proxy inverso para servir la aplicación React y redirigir las solicitudes API al backend.

## Nuevas Tecnologías Implementadas

### 1. Frontend
- **React**: Framework JavaScript para construir interfaces de usuario.
- **React Router DOM**: Manejo de rutas en la aplicación React.
- **Vite**: Herramienta de construcción rápida para aplicaciones JavaScript modernas.
- **Context API**: Para gestión de estado global (autenticación).

### 2. Backend
- **Django REST Framework**: Extensión de Django para crear APIs RESTful.
- **Django CORS Headers**: Manejo de peticiones de origen cruzado (CORS).
- **Whitenoise**: Servir archivos estáticos desde Django.

### 3. Infraestructura
- **Docker**: Containerización de la aplicación.
- **Docker Compose**: Orquestación de servicios (web, frontend, base de datos).
- **Nginx**: Servidor web y proxy inverso.
- **PostgreSQL**: Base de datos relacional.

### 4. Autenticación
- **Token Authentication**: Implementado con DRF para la autenticación de API.
- **Verificación por email**: Sistema de verificación de cuentas mediante tokens.

## Estructura de Directorios

```
PataRescata/
├── apppatarescata/          # Aplicación principal de Django
│   ├── api_views.py         # Vistas para la API REST
│   ├── auth_views.py        # Vistas relacionadas con autenticación
│   ├── forms.py             # Formularios Django
│   ├── models.py            # Modelos de datos
│   ├── management/          # Comandos personalizados
│   └── migrations/          # Migraciones de la base de datos
├── frontend/                # Aplicación React
│   ├── public/              # Archivos estáticos públicos
│   ├── src/                 # Código fuente React
│   │   ├── components/      # Componentes React
│   │   ├── context/         # Contextos para gestión de estado
│   │   ├── App.jsx          # Componente principal
│   │   ├── AppRouter.jsx    # Enrutador principal
│   │   └── main.jsx         # Punto de entrada
│   ├── Dockerfile           # Configuración Docker para frontend
│   ├── nginx.conf           # Configuración de Nginx
│   ├── package.json         # Dependencias de Node.js
│   └── vite.config.js       # Configuración de Vite
├── media/                   # Archivos subidos por usuarios
├── patarescata/             # Configuración del proyecto Django
├── static/                  # Archivos estáticos
├── templates/               # Templates HTML (para las partes que aún no se han migrado)
├── docker-compose.yml       # Configuración de Docker Compose
├── dockerfile               # Configuración Docker para backend
└── requirements.txt         # Dependencias de Python
```

## Cómo Inicializar el Proyecto

### Requisitos Previos
- Docker y Docker Compose instalados
- Git

### Pasos de Inicialización

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/NashoWarner/PataRescata.git
   cd PataRescata
   ```

2. **Configurar variables de entorno (opcional):**
   - Si necesitas personalizar configuraciones, puedes crear un archivo `.env` en la raíz del proyecto.
   - Las variables de entorno ya están configuradas con valores predeterminados en `docker-compose.yml`.

3. **Construir e iniciar los contenedores:**
   ```bash
   docker-compose up --build
   ```
   Este comando:
   - Construirá las imágenes Docker para el backend y frontend
   - Iniciará la base de datos PostgreSQL
   - Aplicará las migraciones de Django
   - Creará un superusuario predeterminado (admin/admin123)
   - Cargará datos de prueba (productos)
   - Iniciará el servidor de desarrollo Django y el servidor Nginx

4. **Acceder a la aplicación:**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000/api
   - Admin Django: http://localhost:8000/admin

5. **Credenciales predeterminadas:**
   - Usuario administrador: `admin@example.com`
   - Contraseña: `admin123`

### Desarrollo y Mantenimiento

#### Trabajar en el Backend

1. Hacer cambios en los archivos de Django
2. Los cambios se reflejan automáticamente gracias al modo de desarrollo de Django

#### Trabajar en el Frontend

**Opción 1: A través de Docker**
```bash
# Reconstruir solo el contenedor frontend
docker-compose up -d --build frontend
```

**Opción 2: Desarrollo local (recomendado para frontend)**
```bash
cd frontend
npm install
npm run dev
```
Esto iniciará un servidor de desarrollo Vite en `http://localhost:5173` con recarga en caliente.

## Explicación de Componentes Claves

### Backend Django REST Framework

El backend proporciona una API RESTful que sirve datos a la aplicación frontend. Principales endpoints:

- `/api/mascotas/`: CRUD para mascotas
- `/api/productos/`: CRUD para productos
- `/api/articulos/`: CRUD para artículos del blog
- `/api/adopciones/`: CRUD para solicitudes de adopción

Endpoints de autenticación:
- `/api/login/`: Inicio de sesión
- `/api/logout/`: Cierre de sesión
- `/api/registro/adoptante/`: Registro de adoptantes
- `/api/registro/fundacion/`: Registro de fundaciones
- `/api/verificar-cuenta/<token>/`: Verificación de cuenta
- `/api/perfil/`: Obtener o actualizar perfil de usuario
- `/api/eliminar-cuenta/`: Eliminar cuenta de usuario

### Frontend React

La aplicación frontend está construida con React y utiliza React Router para la navegación. Componentes principales:

- `App.jsx`: Componente principal que contiene el contexto de autenticación
- `AppRouter.jsx`: Define las rutas de la aplicación
- `AuthContext.jsx`: Maneja el estado de autenticación del usuario
- Componentes de página: `Home`, `Login`, `FAQ`, `Eventos`, etc.

### Docker y Docker Compose

El archivo `docker-compose.yml` define tres servicios:

1. **db**: Base de datos PostgreSQL
   - Persiste datos a través de un volumen Docker

2. **web**: Backend Django
   - Ejecuta migraciones, crea superusuario y inicia el servidor
   - Expone el puerto 8000

3. **frontend**: Frontend React con Nginx
   - Construye la aplicación React y la sirve con Nginx
   - Actúa como proxy para redirigir las solicitudes API al backend
   - Expone el puerto 8080

## Mejoras y Futuro Desarrollo

- **Migración completa**: Finalizar la migración de todos los templates Django a componentes React
- **Pruebas automatizadas**: Implementar pruebas unitarias y de integración
- **CI/CD**: Configurar integración y despliegue continuos
- **PWA**: Convertir la aplicación en una Progressive Web App
- **Optimización de rendimiento**: Implementar lazy loading y optimizar la carga de recursos

## Notas Importantes

- La aplicación utiliza autenticación basada en tokens para la comunicación entre frontend y backend
- Las imágenes subidas por los usuarios se guardan en el directorio `media/`
- La configuración de correo electrónico está configurada para usar Gmail (requiere actualizar las credenciales)
- La rama principal de desarrollo es `Asistente-virtual`

---

Desarrollado con ❤️ para PataRescata
