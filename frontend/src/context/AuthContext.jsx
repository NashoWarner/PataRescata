import React, { createContext, useState, useEffect, useContext } from 'react';

// Crear el contexto de autenticación
const AuthContext = createContext(null);

// Hook personalizado para utilizar el contexto de autenticación
export const useAuth = () => useContext(AuthContext);

// Proveedor del contexto de autenticación
export const AuthProvider = ({ children }) => {
  // Estado para almacenar la información del usuario autenticado
  const [currentUser, setCurrentUser] = useState(null);
  // Estado para controlar si se está cargando la información del usuario
  const [isLoading, setIsLoading] = useState(true);

  // Efecto para cargar la información del usuario desde localStorage al iniciar
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const userType = localStorage.getItem('userType');
    const userName = localStorage.getItem('userName');
    const userData = localStorage.getItem('userData');
    
    if (token && userType) {
      try {
        setCurrentUser({
          token,
          userType,
          userName,
          ...(userData ? JSON.parse(userData) : {})
        });
        
        // Opcionalmente, verificar la validez del token con el backend
        verifyToken(token);
      } catch (error) {
        console.error('Error parsing user data', error);
      }
    }
    
    setIsLoading(false);
  }, []);
  
  // Verificar si el token almacenado es válido
  const verifyToken = async (token) => {
    try {
      const response = await fetch('/api/auth/perfil/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      
      if (!response.ok) {
        // Si el token no es válido, cerrar sesión
        logout();
      }
    } catch (error) {
      console.error('Error al verificar el token:', error);
    }
  };

  // Función para iniciar sesión
  const login = async (credentials, userType) => {
    // Simulación de una solicitud a la API
    try {
      // Aquí se haría la llamada real a la API
      // const response = await fetch('/api/auth/login', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ ...credentials, userType })
      // });
      // const data = await response.json();
      
      // Simulamos una respuesta exitosa
      const data = {
        token: 'fake-token-for-testing',
        userType,
        userName: credentials.email.split('@')[0],
        email: credentials.email
      };
      
      // Guardar la información en localStorage
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('userType', data.userType);
      localStorage.setItem('userName', data.userName);
      localStorage.setItem('userData', JSON.stringify({
        name: data.userName,
        email: data.email
      }));
      
      // Actualizar el estado
      setCurrentUser({
        token: data.token,
        userType: data.userType,
        userName: data.userName,
        email: data.email
      });
      
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.message || 'Error al iniciar sesión' 
      };
    }
  };

  // Función para registrarse
  const register = async (userData, userType) => {
    try {
      // Aquí se haría la llamada real a la API
      // const response = await fetch(`/api/auth/register/${userType}`, {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(userData)
      // });
      // const data = await response.json();
      
      // Simulamos una respuesta exitosa
      return { 
        success: true,
        message: 'Registro exitoso. Por favor revisa tu correo para verificar tu cuenta.' 
      };
    } catch (error) {
      return { 
        success: false, 
        error: error.message || 'Error al registrarse' 
      };
    }
  };

  // Función para cerrar sesión
  const logout = async () => {
    try {
      const token = localStorage.getItem('authToken');
      
      if (token) {
        // Notificar al backend sobre el cierre de sesión
        await fetch('/api/auth/logout/', {
          method: 'POST',
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
          },
        }).catch(error => console.error('Error al notificar cierre de sesión:', error));
      }
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    } finally {
      // Limpiar almacenamiento local
      localStorage.removeItem('authToken');
      localStorage.removeItem('userType');
      localStorage.removeItem('userName');
      localStorage.removeItem('userData');
      
      // Actualizar estado
      setCurrentUser(null);
    }
  };

  // Valor que será proporcionado por el contexto
  const value = {
    currentUser,
    isLoading,
    login,
    register,
    logout,
    isAuthenticated: !!currentUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
