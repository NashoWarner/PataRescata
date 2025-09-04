import React, { useState } from 'react';
import './Login.css';
import { useNavigate, Link } from 'react-router-dom';

function Login({ userType = "adoptante" }) {
  const [credentials, setCredentials] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Error al iniciar sesión');
      }

      // Guardar el token en localStorage
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('userType', data.user_type);
      localStorage.setItem('userName', data.user_name);

      // Redireccionar según el tipo de usuario
      if (data.user_type === 'fundacion') {
        navigate('/perfil-fundacion');
      } else {
        navigate('/perfil');
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="card-header">
          <h1>
            {userType === 'fundacion' ? (
              <><i className="fas fa-building"></i> Iniciar Sesión Fundación</>
            ) : (
              <><i className="fas fa-heart"></i> Iniciar Sesión Adoptante</>
            )}
          </h1>
          <p>Accede a tu cuenta para continuar</p>
        </div>

        <div className="card-body">
          {error && (
            <div className="message error">
              <i className="fas fa-exclamation-circle"></i> {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">
                <i className="fas fa-envelope"></i> Correo Electrónico
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={credentials.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">
                <i className="fas fa-lock"></i> Contraseña
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={credentials.password}
                onChange={handleChange}
                required
              />
            </div>

            <button 
              type="submit" 
              className="btn-login" 
              disabled={isLoading}
            >
              {isLoading ? (
                <span><i className="fas fa-spinner fa-spin"></i> Iniciando...</span>
              ) : (
                <span><i className="fas fa-sign-in-alt"></i> Iniciar Sesión</span>
              )}
            </button>
          </form>

          <div className="divider">
            <span>¿No tienes una cuenta?</span>
          </div>

          <Link 
            to={userType === 'fundacion' ? '/registro/fundacion' : '/registro/adoptante'} 
            className="btn-register"
          >
            <i className="fas fa-plus"></i> Registrarse
          </Link>

          <div className="select-type">
            <Link to="/seleccionar-cuenta">
              <i className="fas fa-arrow-left"></i> Volver a selección de cuenta
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
