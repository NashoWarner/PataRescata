import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  // Función para manejar la suscripción al newsletter
  const handleNewsletterSubmit = (e) => {
    e.preventDefault();
    // Aquí iría la lógica para procesar la suscripción
    alert('¡Gracias por suscribirte a nuestro newsletter!');
    e.target.reset();
  };

  // Función para volver arriba cuando se hace clic en el botón
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  return (
    <footer className="footer">
      <div className="footer-content">
        {/* Sección Principal del Footer */}
        <div className="footer-main">
          <div className="footer-section">
            <div className="footer-logo">
              <div className="logo-icon">
                <i className="fas fa-paw"></i>
              </div>
              <h3>PataRescata</h3>
              <p>Conectando corazones con patas</p>
            </div>
            <div className="social-links">
              <a href="https://facebook.com" className="social-link" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                <i className="fab fa-facebook-f"></i>
              </a>
              <a href="https://instagram.com" className="social-link" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                <i className="fab fa-instagram"></i>
              </a>
              <a href="https://twitter.com" className="social-link" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="https://youtube.com" className="social-link" target="_blank" rel="noopener noreferrer" aria-label="YouTube">
                <i className="fab fa-youtube"></i>
              </a>
            </div>
          </div>

          <div className="footer-section">
            <h4>Adopción</h4>
            <ul className="footer-links">
              <li><Link to="/mascotas">Buscar Mascotas</Link></li>
              <li><Link to="/blog">Guías de Adopción</Link></li>
              <li><Link to="/faq">Preguntas Frecuentes</Link></li>
              <li><Link to="/fundaciones">Fundaciones</Link></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Recursos</h4>
            <ul className="footer-links">
              <li><Link to="/blog">Blog Educativo</Link></li>
              <li><Link to="/tienda">Productos para Mascotas</Link></li>
              <li><Link to="/cuidado-animal">Cuidado Animal</Link></li>
              <li><Link to="/eventos">Eventos</Link></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Contacto</h4>
            <div className="contact-info">
              <div className="contact-item">
                <i className="fas fa-map-marker-alt"></i>
                <span>Santiago de Chile</span>
              </div>
              <div className="contact-item">
                <i className="fas fa-phone"></i>
                <span>+56 9 64484168</span>
              </div>
              <div className="contact-item">
                <i className="fas fa-envelope"></i>
                <span>info@patarescata.cl</span>
              </div>
            </div>
          </div>
        </div>

        {/* Sección de Newsletter */}
        <div className="newsletter-section">
          <div className="newsletter-content">
            <h4>¡Únete a nuestra comunidad!</h4>
            <p>Recibe noticias sobre mascotas disponibles y consejos de cuidado</p>
            <form className="newsletter-form" onSubmit={handleNewsletterSubmit}>
              <input type="email" placeholder="Tu correo electrónico" required />
              <button type="submit">
                <i className="fas fa-paper-plane"></i>
                Suscribirse
              </button>
            </form>
          </div>
        </div>

        {/* Línea divisoria */}
        <div className="footer-divider"></div>

        {/* Sección inferior */}
        <div className="footer-bottom">
          <div className="footer-bottom-content">
            <div className="copyright">
              <p>&copy; {new Date().getFullYear()} PataRescata. Todos los derechos reservados.</p>
              <p>Proyecto desarrollado con ❤️ para conectar mascotas con hogares amorosos</p>
            </div>
            <div className="footer-bottom-links">
              <Link to="/privacidad">Política de Privacidad</Link>
              <Link to="/terminos">Términos de Servicio</Link>
              <Link to="/cookies">Cookies</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Botón de volver arriba */}
      <button className="back-to-top" onClick={scrollToTop} aria-label="Volver arriba">
        <i className="fas fa-chevron-up"></i>
      </button>
    </footer>
  );
};

export default Footer;
