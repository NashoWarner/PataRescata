import React from 'react';
import './Nosotros.css';

const Nosotros = () => {
  // Datos del equipo
  const equipo = [
    {
      nombre: 'María Rodríguez',
      cargo: 'Fundadora & CEO',
      imagen: '/static/images/team-member1.jpg',
      descripcion: 'María fundó PataRescata con la visión de crear una plataforma que conecte a mascotas necesitadas con hogares amorosos. Tiene más de 10 años de experiencia en protección animal.'
    },
    {
      nombre: 'Carlos Martínez',
      cargo: 'Director de Operaciones',
      imagen: '/static/images/team-member2.jpg',
      descripcion: 'Carlos se encarga de coordinar las relaciones con fundaciones y refugios. Su experiencia en logística garantiza un proceso de adopción fluido y eficiente.'
    },
    {
      nombre: 'Ana Gómez',
      cargo: 'Coordinadora de Adopciones',
      imagen: '/static/images/team-member3.jpg',
      descripcion: 'Ana supervisa cada proceso de adopción para garantizar que las mascotas encuentren el hogar perfecto. Su formación en comportamiento animal es clave para el éxito.'
    },
    {
      nombre: 'Daniel Torres',
      cargo: 'Desarrollador Web',
      imagen: '/static/images/team-member4.jpg',
      descripcion: 'Daniel es el responsable de mantener nuestra plataforma funcionando sin problemas. Su pasión por los animales y la tecnología hacen de él un miembro invaluable.'
    }
  ];

  // Datos de los valores
  const valores = [
    {
      icono: 'fa-heart',
      titulo: 'Compasión',
      descripcion: 'Actuamos con empatía hacia todos los animales y personas involucradas en el proceso de adopción.'
    },
    {
      icono: 'fa-handshake',
      titulo: 'Responsabilidad',
      descripcion: 'Nos comprometemos a seguir altos estándares éticos en todas nuestras operaciones y procesos.'
    },
    {
      icono: 'fa-users',
      titulo: 'Comunidad',
      descripcion: 'Fomentamos una comunidad comprometida con el bienestar animal y la adopción responsable.'
    },
    {
      icono: 'fa-lightbulb',
      titulo: 'Innovación',
      descripcion: 'Buscamos constantemente nuevas formas de mejorar nuestra plataforma y ampliar nuestro impacto.'
    },
    {
      icono: 'fa-shield-alt',
      titulo: 'Protección',
      descripcion: 'Nuestro trabajo está orientado a garantizar la seguridad y el bienestar de todas las mascotas.'
    }
  ];

  return (
    <div className="nosotros-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Sobre Nosotros</h1>
          <p className="hero-subtitle">
            Conoce al equipo detrás de PataRescata, nuestra misión, visión y los valores que guían nuestro trabajo diario para mejorar la vida de los animales en Chile.
          </p>
        </div>
      </section>

      {/* Contenido Principal */}
      <div className="main-content">
        
        {/* Sección Misión y Visión */}
        <section className="section">
          <h2 className="section-title">Nuestra Misión y Visión</h2>
          
          <div className="mission-vision">
            <div className="mission-card">
              <div className="card-icon">
                <i className="fas fa-bullseye"></i>
              </div>
              <h3 className="card-title">Misión</h3>
              <p className="card-description">
                Facilitar la conexión entre mascotas que necesitan un hogar y personas dispuestas a adoptar, promoviendo la adopción responsable y el bienestar animal en todo Chile.
              </p>
            </div>
            
            <div className="vision-card">
              <div className="card-icon">
                <i className="fas fa-eye"></i>
              </div>
              <h3 className="card-title">Visión</h3>
              <p className="card-description">
                Convertirnos en la plataforma líder de adopción en Chile, donde cada mascota tenga la oportunidad de encontrar un hogar amoroso y cada persona pueda encontrar a su compañero perfecto.
              </p>
            </div>
          </div>
          
          <div className="historia">
            <h3>Nuestra Historia</h3>
            <p>
              PataRescata nació en 2020 como respuesta a la necesidad de centralizar y facilitar los procesos de adopción en Chile. Comenzamos como un pequeño proyecto con apenas un puñado de fundaciones asociadas, pero rápidamente crecimos gracias al apoyo de una comunidad comprometida con el bienestar animal.
            </p>
            <p>
              A lo largo de estos años, hemos facilitado miles de adopciones exitosas, creando conexiones perfectas entre mascotas y familias. Nuestro equipo ha crecido, nuestros procesos han mejorado, pero nuestra pasión sigue siendo la misma: dar a cada animal la oportunidad de tener el hogar que merece.
            </p>
            <p>
              Hoy, PataRescata es mucho más que una plataforma de adopción; somos una comunidad que trabaja incansablemente por el bienestar animal y la promoción de la adopción responsable en todo el país.
            </p>
          </div>
        </section>
        
        {/* Sección Valores */}
        <section className="section">
          <h2 className="section-title">Nuestros Valores</h2>
          
          <div className="values-section">
            <p className="values-intro">
              Estos son los principios fundamentales que guían nuestras acciones y decisiones día a día:
            </p>
            
            <div className="values-grid">
              {valores.map((valor, index) => (
                <div className="value-item" key={index}>
                  <div className="value-icon">
                    <i className={`fas ${valor.icono}`}></i>
                  </div>
                  <h3 className="value-title">{valor.titulo}</h3>
                  <p className="value-description">{valor.descripcion}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
        
        {/* Sección Equipo */}
        <section className="section team-section">
          <h2 className="section-title">Nuestro Equipo</h2>
          
          <p className="team-intro">
            Somos un equipo diverso de profesionales apasionados por el bienestar animal. Cada uno de nosotros aporta habilidades únicas, pero todos compartimos el mismo objetivo: conectar mascotas con hogares amorosos.
          </p>
          
          <div className="team-grid">
            {equipo.map((miembro, index) => (
              <div className="team-member" key={index}>
                <div className="member-image">
                  <img src={miembro.imagen} alt={miembro.nombre} />
                </div>
                <div className="member-info">
                  <h3 className="member-name">{miembro.nombre}</h3>
                  <p className="member-role">{miembro.cargo}</p>
                  <p className="member-description">{miembro.descripcion}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
        
        {/* Sección Contacto */}
        <section className="contact-section">
          <div className="contact-container">
            <h2>¿Quieres ser parte de nuestro equipo?</h2>
            <p>
              Estamos siempre buscando personas apasionadas que quieran sumarse a nuestra misión. 
              Si crees en el bienestar animal y quieres hacer una diferencia, ¡nos encantaría conocerte!
            </p>
            <button className="contact-btn">
              <i className="fas fa-envelope"></i> Contáctanos
            </button>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Nosotros;
