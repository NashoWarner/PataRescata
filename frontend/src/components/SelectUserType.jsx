import React from 'react';
import { Link } from 'react-router-dom';
import './SelectUserType.css';

const SelectUserType = () => {
  return (
    <div className="select-user-type-container">
      <div className="select-user-type-content">
        <h1 className="select-title">¡Bienvenido a PataRescata!</h1>
        <p className="select-description">
          Selecciona el tipo de cuenta con la que deseas continuar
        </p>
        
        <div className="user-types">
          <div className="user-type-card">
            <div className="card-icon">
              <i className="fas fa-user"></i>
            </div>
            <h2>Soy Adoptante</h2>
            <p>
              Busco adoptar una mascota y darle un hogar lleno de amor.
            </p>
            <div className="card-actions">
              <Link to="/login/adoptante" className="btn-login">
                <i className="fas fa-sign-in-alt"></i> Iniciar sesión
              </Link>
              <Link to="/registro/adoptante" className="btn-register">
                <i className="fas fa-user-plus"></i> Registrarme
              </Link>
            </div>
          </div>
          
          <div className="user-type-card">
            <div className="card-icon">
              <i className="fas fa-building"></i>
            </div>
            <h2>Soy Fundación</h2>
            <p>
              Representamos una organización que protege y busca hogares para mascotas.
            </p>
            <div className="card-actions">
              <Link to="/login/fundacion" className="btn-login">
                <i className="fas fa-sign-in-alt"></i> Iniciar sesión
              </Link>
              <Link to="/registro/fundacion" className="btn-register">
                <i className="fas fa-user-plus"></i> Registrarme
              </Link>
            </div>
          </div>
        </div>
        
        <div className="back-to-home">
          <Link to="/">
            <i className="fas fa-arrow-left"></i> Volver a la página principal
          </Link>
        </div>
      </div>
    </div>
  );
};

export default SelectUserType;
