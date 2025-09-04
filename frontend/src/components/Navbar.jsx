import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './Navbar.css';
import { useAuth } from '../context/AuthContext';
import logo from '../assets/images/Logo_pata_blanco.png';

const Navbar = () => {
  const { currentUser, logout, isAuthenticated } = useAuth();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // Efecto para detectar el scroll
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/');
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    }
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className={`navbar navbar-expand-lg ${isScrolled ? 'navbar-scrolled' : ''}`}>
      <div className="container">
        <Link to="/" className="navbar-brand d-flex align-items-center">
          <img src={logo} alt="PataRescata Logo" className="me-2" height="40" />
          <span>PataRescata</span>
        </Link>
        
        <button 
          className="navbar-toggler" 
          type="button" 
          onClick={toggleMobileMenu}
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        
        <div className={`collapse navbar-collapse ${isMobileMenuOpen ? 'show' : ''}`}>
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <Link 
                to="/" 
                className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
              >
                Inicio
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/mascotas" 
                className={`nav-link ${location.pathname === '/mascotas' ? 'active' : ''}`}
              >
                Mascotas
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/nosotros" 
                className={`nav-link ${location.pathname === '/nosotros' ? 'active' : ''}`}
              >
                Nosotros
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/blog" 
                className={`nav-link ${location.pathname === '/blog' ? 'active' : ''}`}
              >
                Blog
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/faq" 
                className={`nav-link ${location.pathname === '/faq' ? 'active' : ''}`}
              >
                Preguntas Frecuentes
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/eventos" 
                className={`nav-link ${location.pathname === '/eventos' ? 'active' : ''}`}
              >
                Eventos
              </Link>
            </li>
          </ul>
          
          <div className="d-flex">
            {isAuthenticated ? (
              <div className="dropdown">
                <button 
                  className="btn btn-outline-light dropdown-toggle" 
                  type="button" 
                  id="profileDropdown" 
                  data-bs-toggle="dropdown" 
                  aria-expanded="false"
                >
                  <i className="bi bi-person-circle me-2"></i>
                  {currentUser?.userName || 'Usuario'}
                </button>
                <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="profileDropdown">
                  <li>
                    <Link 
                      to={currentUser?.userType === 'fundacion' ? '/perfil-fundacion' : '/perfil'} 
                      className="dropdown-item"
                    >
                      <i className="bi bi-person me-2"></i>Mi Perfil
                    </Link>
                  </li>
                  {currentUser?.userType === 'fundacion' && (
                    <li>
                      <Link to="/agregar-mascota" className="dropdown-item">
                        <i className="bi bi-plus-circle me-2"></i>Agregar Mascota
                      </Link>
                    </li>
                  )}
                  <li>
                    <Link to="/mis-solicitudes" className="dropdown-item">
                      <i className="bi bi-list-check me-2"></i>Mis Solicitudes
                    </Link>
                  </li>
                  <li><hr className="dropdown-divider" /></li>
                  <li>
                    <button onClick={handleLogout} className="dropdown-item">
                      <i className="bi bi-box-arrow-right me-2"></i>Cerrar Sesión
                    </button>
                  </li>
                </ul>
              </div>
            ) : (
              <Link to="/seleccionar-cuenta" className="btn btn-outline-light">
                <i className="bi bi-person me-2"></i>Iniciar Sesión
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
