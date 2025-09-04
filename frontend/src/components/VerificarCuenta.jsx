import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import './VerificarCuenta.css';

const VerificarCuenta = () => {
  const { token } = useParams();
  const [status, setStatus] = useState('loading'); // loading, success, error
  const [message, setMessage] = useState('');

  useEffect(() => {
    const verificarToken = async () => {
      try {
        const response = await fetch(`/api/auth/verificar/${token}/`);
        const data = await response.json();
        
        if (response.ok) {
          setStatus('success');
          setMessage(data.detail || 'Cuenta verificada correctamente');
        } else {
          setStatus('error');
          setMessage(data.detail || 'Error al verificar la cuenta');
        }
      } catch (error) {
        setStatus('error');
        setMessage('Error de conexión al verificar la cuenta');
      }
    };

    verificarToken();
  }, [token]);

  return (
    <div className="verificar-container">
      <div className="verificar-card">
        {status === 'loading' && (
          <div className="verificar-loading">
            <div className="spinner"></div>
            <p>Verificando tu cuenta...</p>
          </div>
        )}
        
        {status === 'success' && (
          <div className="verificar-success">
            <div className="icon-circle success">
              <i className="fas fa-check"></i>
            </div>
            <h1>¡Cuenta Verificada!</h1>
            <p>{message}</p>
            <p className="info-text">
              Ahora puedes acceder a todas las funciones de PataRescata.
            </p>
            <div className="action-buttons">
              <Link to="/login/adoptante" className="btn-primary">
                <i className="fas fa-sign-in-alt"></i> Iniciar Sesión como Adoptante
              </Link>
              <Link to="/login/fundacion" className="btn-secondary">
                <i className="fas fa-sign-in-alt"></i> Iniciar Sesión como Fundación
              </Link>
            </div>
          </div>
        )}
        
        {status === 'error' && (
          <div className="verificar-error">
            <div className="icon-circle error">
              <i className="fas fa-exclamation-triangle"></i>
            </div>
            <h1>Error de Verificación</h1>
            <p>{message}</p>
            <p className="info-text">
              El enlace de verificación puede haber expirado o ya ha sido utilizado.
            </p>
            <div className="action-buttons">
              <Link to="/" className="btn-primary">
                <i className="fas fa-home"></i> Ir a la Página Principal
              </Link>
              <Link to="/seleccionar-cuenta" className="btn-secondary">
                <i className="fas fa-redo"></i> Intentar de Nuevo
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VerificarCuenta;
