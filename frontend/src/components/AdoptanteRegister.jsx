import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Register.css';

const AdoptanteRegister = () => {
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    password: '',
    password2: '',
    rut: '',
    direccion: '',
    telefono: ''
  });
  
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
    
    // Limpiar error específico al modificar el campo
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: ''
      });
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    // Validar nombre
    if (!formData.nombre.trim()) {
      newErrors.nombre = 'El nombre es obligatorio';
    }
    
    // Validar email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Correo electrónico inválido';
    }
    
    // Validar contraseña
    if (formData.password.length < 8) {
      newErrors.password = 'La contraseña debe tener al menos 8 caracteres';
    }
    
    // Validar confirmación de contraseña
    if (formData.password !== formData.password2) {
      newErrors.password2 = 'Las contraseñas no coinciden';
    }
    
    // Validar RUT (formato básico)
    const rutRegex = /^\d{1,8}-[0-9kK]$/;
    if (!rutRegex.test(formData.rut)) {
      newErrors.rut = 'Formato de RUT inválido (ej: 12345678-9)';
    }
    
    // Validar dirección
    if (!formData.direccion.trim()) {
      newErrors.direccion = 'La dirección es obligatoria';
    }
    
    // Validar teléfono (formato básico)
    const phoneRegex = /^\+?[0-9]{9,12}$/;
    if (!phoneRegex.test(formData.telefono)) {
      newErrors.telefono = 'Formato de teléfono inválido';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsLoading(true);
    setMessage('');
    
    try {
      const response = await fetch('/api/auth/registro/adoptante/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        // Manejar errores del servidor
        if (typeof data === 'object') {
          setErrors(data);
        } else {
          setMessage('Error al registrar: ' + JSON.stringify(data));
        }
        return;
      }
      
      // Registro exitoso
      setMessage('Registro exitoso. Por favor verifica tu correo electrónico.');
      setTimeout(() => {
        navigate('/login/adoptante');
      }, 3000);
      
    } catch (error) {
      setMessage('Error de conexión: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <div className="register-header">
          <h1><i className="fas fa-paw"></i> Registro de Adoptante</h1>
          <p>Completa tus datos para crear una cuenta</p>
        </div>
        
        <div className="register-body">
          {message && (
            <div className={`message ${message.includes('exitoso') ? 'success' : 'error'}`}>
              <i className={`fas ${message.includes('exitoso') ? 'fa-check-circle' : 'fa-exclamation-circle'}`}></i> {message}
            </div>
          )}
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="nombre">
                <i className="fas fa-user"></i> Nombre Completo*
              </label>
              <input 
                type="text" 
                id="nombre" 
                name="nombre" 
                value={formData.nombre}
                onChange={handleChange}
                className={errors.nombre ? 'error' : ''}
                required
              />
              {errors.nombre && <span className="error-message">{errors.nombre}</span>}
            </div>
            
            <div className="form-group">
              <label htmlFor="email">
                <i className="fas fa-envelope"></i> Correo Electrónico*
              </label>
              <input 
                type="email" 
                id="email" 
                name="email" 
                value={formData.email}
                onChange={handleChange}
                className={errors.email ? 'error' : ''}
                required
              />
              {errors.email && <span className="error-message">{errors.email}</span>}
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="password">
                  <i className="fas fa-lock"></i> Contraseña*
                </label>
                <input 
                  type="password" 
                  id="password" 
                  name="password" 
                  value={formData.password}
                  onChange={handleChange}
                  className={errors.password ? 'error' : ''}
                  required
                />
                {errors.password && <span className="error-message">{errors.password}</span>}
              </div>
              
              <div className="form-group">
                <label htmlFor="password2">
                  <i className="fas fa-lock"></i> Confirmar Contraseña*
                </label>
                <input 
                  type="password" 
                  id="password2" 
                  name="password2" 
                  value={formData.password2}
                  onChange={handleChange}
                  className={errors.password2 ? 'error' : ''}
                  required
                />
                {errors.password2 && <span className="error-message">{errors.password2}</span>}
              </div>
            </div>
            
            <div className="form-group">
              <label htmlFor="rut">
                <i className="fas fa-id-card"></i> RUT*
              </label>
              <input 
                type="text" 
                id="rut" 
                name="rut" 
                placeholder="12345678-9"
                value={formData.rut}
                onChange={handleChange}
                className={errors.rut ? 'error' : ''}
                required
              />
              {errors.rut && <span className="error-message">{errors.rut}</span>}
            </div>
            
            <div className="form-group">
              <label htmlFor="direccion">
                <i className="fas fa-map-marker-alt"></i> Dirección*
              </label>
              <input 
                type="text" 
                id="direccion" 
                name="direccion" 
                value={formData.direccion}
                onChange={handleChange}
                className={errors.direccion ? 'error' : ''}
                required
              />
              {errors.direccion && <span className="error-message">{errors.direccion}</span>}
            </div>
            
            <div className="form-group">
              <label htmlFor="telefono">
                <i className="fas fa-phone"></i> Teléfono*
              </label>
              <input 
                type="tel" 
                id="telefono" 
                name="telefono" 
                placeholder="+56912345678"
                value={formData.telefono}
                onChange={handleChange}
                className={errors.telefono ? 'error' : ''}
                required
              />
              {errors.telefono && <span className="error-message">{errors.telefono}</span>}
            </div>
            
            <button 
              type="submit" 
              className="btn-register-submit" 
              disabled={isLoading}
            >
              {isLoading ? (
                <span><i className="fas fa-spinner fa-spin"></i> Registrando...</span>
              ) : (
                <span><i className="fas fa-user-plus"></i> Crear Cuenta</span>
              )}
            </button>
          </form>
          
          <div className="login-link">
            ¿Ya tienes una cuenta? <Link to="/login/adoptante">Iniciar Sesión</Link>
          </div>
          
          <div className="back-link">
            <Link to="/seleccionar-cuenta">
              <i className="fas fa-arrow-left"></i> Volver a selección de cuenta
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdoptanteRegister;
