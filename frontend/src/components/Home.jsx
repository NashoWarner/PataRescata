import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const [mascotas, setMascotas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estadísticas 
  const estadisticas = [
    { numero: '2,500+', etiqueta: 'Mascotas Adoptadas' },
    { numero: '500+', etiqueta: 'Fundaciones Asociadas' },
    { numero: '10,000+', etiqueta: 'Usuarios Registrados' },
    { numero: '20+', etiqueta: 'Ciudades en Chile' }
  ];

  // Características
  const caracteristicas = [
    {
      icono: 'fa-paw',
      titulo: 'Adopción Segura',
      descripcion: 'Proceso de adopción verificado y seguro para asegurar el bienestar de las mascotas.'
    },
    {
      icono: 'fa-home',
      titulo: 'Hogares Verificados',
      descripcion: 'Verificamos que cada mascota vaya a un hogar donde recibirá el cuidado que merece.'
    },
    {
      icono: 'fa-heart',
      titulo: 'Comunidad Comprometida',
      descripcion: 'Una comunidad comprometida con el rescate y bienestar animal en todo Chile.'
    }
  ];

  useEffect(() => {
    // Simulación de carga de mascotas destacadas desde API
    const fetchMascotas = async () => {
      try {
        // Aquí se haría la llamada real a la API
        // const response = await fetch('/api/mascotas/destacadas');
        // const data = await response.json();
        
        // Por ahora simulamos datos
        const data = [
          {
            id: 1,
            nombre: 'Luna',
            edad: '2 años',
            imagen: '/static/images/dog1.jpg',
            especie: 'Perro',
            descripcion: 'Luna es una perrita muy cariñosa y juguetona que busca un hogar amoroso.'
          },
          {
            id: 2,
            nombre: 'Simba',
            edad: '3 años',
            imagen: '/static/images/dog2.jpg',
            especie: 'Perro',
            descripcion: 'Simba es un perro activo y amigable que adora jugar y correr al aire libre.'
          },
          {
            id: 3,
            nombre: 'Mia',
            edad: '1 año',
            imagen: '/static/images/cat1.jpg',
            especie: 'Gato',
            descripcion: 'Mia es una gatita tranquila y cariñosa que busca un hogar tranquilo.'
          },
          {
            id: 4,
            nombre: 'Rocky',
            edad: '4 años',
            imagen: '/static/images/dog3.jpg',
            especie: 'Perro',
            descripcion: 'Rocky es un perro grande y protector, ideal para familias con niños.'
          }
        ];
        
        setMascotas(data);
        setLoading(false);
      } catch (err) {
        setError('Error al cargar mascotas destacadas');
        setLoading(false);
        console.error(err);
      }
    };

    fetchMascotas();
  }, []);

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Encuentra a tu compañero perfecto</h1>
          <p className="hero-subtitle">
            Conectamos mascotas que necesitan un hogar con personas dispuestas a brindarles amor y cuidado.
            Juntos podemos transformar vidas, una adopción a la vez.
          </p>
          <div className="hero-buttons">
            <Link to="/adoptar" className="cta-button cta-primary">
              <i className="fas fa-paw"></i> Adoptar Mascota
            </Link>
            <Link to="/fundaciones" className="cta-button cta-secondary">
              <i className="fas fa-hands-helping"></i> Conocer Fundaciones
            </Link>
          </div>
        </div>
      </section>

      {/* Sección de Estadísticas */}
      <section className="stats-section">
        <div className="stats-container">
          {estadisticas.map((stat, index) => (
            <div className="stat-item" key={index}>
              <span className="stat-number">{stat.numero}</span>
              <span className="stat-label">{stat.etiqueta}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Sección de Características */}
      <section className="features-section">
        <div className="features-container">
          <h2 className="section-title">¿Por qué adoptar con PataRescata?</h2>
          <div className="features-grid">
            {caracteristicas.map((feature, index) => (
              <div className="feature-card" key={index}>
                <div className="feature-icon">
                  <i className={`fas ${feature.icono}`}></i>
                </div>
                <h3 className="feature-title">{feature.titulo}</h3>
                <p className="feature-description">{feature.descripcion}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Sección de Mascotas Destacadas */}
      <section className="pets-section">
        <div className="pets-container">
          <h2 className="section-title">Mascotas Destacadas</h2>
          
          {loading && <div className="loading">Cargando mascotas...</div>}
          {error && <div className="error">{error}</div>}
          
          <div className="pets-grid">
            {mascotas.map(mascota => (
              <div className="pet-card" key={mascota.id}>
                <div className="pet-image-container">
                  <img src={mascota.imagen} alt={mascota.nombre} className="pet-image" />
                </div>
                <div className="pet-info">
                  <h3 className="pet-name">{mascota.nombre}</h3>
                  <p className="pet-details">
                    <span>{mascota.especie} · {mascota.edad}</span>
                    <br />
                    {mascota.descripcion}
                  </p>
                  <Link to={`/mascotas/${mascota.id}`} className="adopt-button">
                    Conocer Más
                  </Link>
                </div>
              </div>
            ))}
          </div>
          
          <div className="view-all-container">
            <Link to="/mascotas" className="view-all-button">
              Ver todas las mascotas <i className="fas fa-arrow-right"></i>
            </Link>
          </div>
        </div>
      </section>

      {/* Sección de CTA */}
      <section className="cta-section">
        <div className="cta-container">
          <h2 className="cta-title">¿Tienes una fundación de rescate animal?</h2>
          <p className="cta-description">
            Únete a nuestra red de fundaciones y aumenta la visibilidad de tus mascotas en adopción.
            Juntos podemos encontrar más hogares para las mascotas que lo necesitan.
          </p>
          <div className="cta-buttons">
            <Link to="/registro-fundacion" className="cta-button-fundacion">
              Registrar mi Fundación <i className="fas fa-arrow-right"></i>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
