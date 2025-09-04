import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './FAQ.css';

const FAQ = () => {
  const [activeItem, setActiveItem] = useState(null);
  
  // Efecto para manejar la animación de entrada para las secciones
  useEffect(() => {
    const sections = document.querySelectorAll('.faq-section, .stats-section, .contact-section');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    });

    sections.forEach(section => {
      section.style.opacity = '0';
      section.style.transform = 'translateY(30px)';
      section.style.transition = 'all 0.6s ease';
      observer.observe(section);
    });

    return () => {
      sections.forEach(section => {
        observer.unobserve(section);
      });
    };
  }, []);
  
  // Función para manejar el clic en un ítem de FAQ
  const handleItemClick = (index) => {
    setActiveItem(activeItem === index ? null : index);
  };

  // Datos de las FAQs
  const adoptionFaqs = [
    {
      question: '¿Cuáles son los requisitos para adoptar una mascota?',
      answer: 'Para adoptar una mascota necesitas: ser mayor de 18 años, tener un hogar estable, comprometerte a cuidar a la mascota de por vida, y pasar por un proceso de evaluación que incluye entrevista y visita domiciliaria.'
    },
    {
      question: '¿Cuánto cuesta adoptar una mascota?',
      answer: 'La adopción en sí es gratuita, pero debes considerar los costos de vacunación, esterilización, microchip y cuidados veterinarios básicos que pueden variar entre $50,000 y $150,000 pesos chilenos.'
    },
    {
      question: '¿Qué mascotas están disponibles para adopción?',
      answer: 'Tenemos perros y gatos de todas las edades, tamaños y razas. Cada mascota viene con su historia y características únicas. Nuestro equipo te ayudará a encontrar la mascota perfecta para tu estilo de vida.'
    },
    {
      question: '¿Cuánto tiempo toma el proceso de adopción?',
      answer: 'El proceso completo puede tomar entre 1-2 semanas. Incluye: aplicación inicial, revisión de documentos, entrevista, visita domiciliaria, y finalmente la firma del contrato de adopción.'
    },
    {
      question: '¿Puedo devolver la mascota si no funciona?',
      answer: 'Sí, pero solo en casos excepcionales y durante los primeros 30 días. Te recomendamos que pienses bien la decisión antes de adoptar, ya que una mascota es un compromiso de por vida.'
    },
    {
      question: '¿Qué incluye la adopción?',
      answer: 'La adopción incluye: mascota esterilizada, vacunas al día, microchip, desparasitación, evaluación veterinaria completa, y orientación post-adopción. También recibirás un kit básico con collar, placa y algunos consejos de cuidado.'
    }
  ];

  // Datos de las estadísticas
  const stats = [
    { number: '500+', label: 'Mascotas Adoptadas' },
    { number: '200+', label: 'Familias Felices' },
    { number: '15+', label: 'Fundaciones Aliadas' },
    { number: '98%', label: 'Tasa de Éxito' }
  ];

  return (
    <div className="faq-container">
      {/* Header de la Página */}
      <div className="page-header">
        <h1 className="page-title">Preguntas Frecuentes</h1>
        <p className="page-subtitle">
          Encuentra respuestas a las preguntas más comunes sobre adopción de mascotas, 
          procesos y cuidados necesarios para darle un hogar amoroso a tu nuevo compañero.
        </p>
      </div>

      {/* Sección de FAQ */}
      <div className="faq-section">
        <h2 className="section-title">Preguntas sobre Adopción</h2>
        <div className="faq-grid">
          {adoptionFaqs.map((faq, index) => (
            <div 
              key={index} 
              className={`faq-item ${activeItem === index ? 'active' : ''}`}
              onClick={() => handleItemClick(index)}
            >
              <div className="faq-question">
                <span>{faq.question}</span>
                <i className={`fas fa-chevron-down ${activeItem === index ? 'rotated' : ''}`}></i>
              </div>
              <div className="faq-answer" style={{ maxHeight: activeItem === index ? '200px' : '0' }}>
                {faq.answer}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Sección de Estadísticas */}
      <div className="stats-section">
        <h2 className="section-title">Nuestro Impacto</h2>
        <div className="stats-grid">
          {stats.map((stat, index) => (
            <div key={index} className="stat-item">
              <div className="stat-number">{stat.number}</div>
              <div className="stat-label">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Sección de Contacto */}
      <div className="contact-section">
        <h3>¿No encontraste tu respuesta?</h3>
        <p>Nuestro equipo está aquí para ayudarte. Contáctanos y te responderemos lo antes posible.</p>
        <div className="contact-buttons">
          <Link to="/nosotros" className="btn btn-primary">
            <i className="fas fa-envelope"></i> Contactar
          </Link>
          <Link to="/" className="btn btn-secondary">
            <i className="fas fa-home"></i> Volver al Inicio
          </Link>
        </div>
      </div>
    </div>
  );
};

export default FAQ;
