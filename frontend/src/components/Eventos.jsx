import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Eventos.css';

const Eventos = () => {
  // Estado para la fecha actual del calendario
  const [currentDate, setCurrentDate] = useState(new Date());
  const [currentMonth, setCurrentMonth] = useState(currentDate.getMonth());
  const [currentYear, setCurrentYear] = useState(currentDate.getFullYear());

  const monthNames = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ];

  // Eventos simulados en fechas específicas
  const eventDates = [
    '2025-09-15', '2025-09-22', '2025-09-29',
    '2025-10-06', '2025-10-13', '2025-10-20'
  ];

  // Verificar si una fecha tiene eventos
  const hasEvents = (date) => {
    const dateString = date.toISOString().split('T')[0];
    return eventDates.includes(dateString);
  };

  // Navegar al mes anterior
  const previousMonth = () => {
    setCurrentMonth(prevMonth => {
      if (prevMonth === 0) {
        setCurrentYear(prevYear => prevYear - 1);
        return 11;
      } else {
        return prevMonth - 1;
      }
    });
  };

  // Navegar al mes siguiente
  const nextMonth = () => {
    setCurrentMonth(prevMonth => {
      if (prevMonth === 11) {
        setCurrentYear(prevYear => prevYear + 1);
        return 0;
      } else {
        return prevMonth + 1;
      }
    });
  };

  // Ir al mes actual
  const goToToday = () => {
    const today = new Date();
    setCurrentMonth(today.getMonth());
    setCurrentYear(today.getFullYear());
  };

  // Generar el calendario
  const renderCalendar = () => {
    const calendarDays = [];
    
    // Agregar encabezados de días
    const dayHeaders = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    dayHeaders.forEach(day => {
      calendarDays.push(
        <div key={`header-${day}`} className="calendar-day-header">
          {day}
        </div>
      );
    });
    
    // Obtener primer día del mes
    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay());
    
    // Generar días del calendario
    for (let i = 0; i < 42; i++) {
      const dayDate = new Date(startDate);
      dayDate.setDate(startDate.getDate() + i);
      
      const isToday = dayDate.toDateString() === new Date().toDateString();
      const isOtherMonth = dayDate.getMonth() !== currentMonth;
      
      calendarDays.push(
        <div 
          key={`day-${i}`} 
          className={`calendar-day ${isOtherMonth ? 'other-month' : ''} ${isToday ? 'today' : ''}`}
        >
          <div className="day-number">{dayDate.getDate()}</div>
          {hasEvents(dayDate) && <div className="event-indicator"></div>}
        </div>
      );
    }
    
    return calendarDays;
  };

  // Efecto para animaciones de entrada
  useEffect(() => {
    const sections = document.querySelectorAll('.calendar-section, .events-section, .upcoming-events, .cta-section');
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
        if (observer && section) {
          observer.unobserve(section);
        }
      });
    };
  }, []);

  // Datos para eventos destacados
  const featuredEvents = [
    {
      date: '15 Septiembre',
      title: 'Feria de Adopción "Amigos Peludos"',
      description: 'Una jornada especial donde podrás conocer a mascotas en busca de hogar. Habrá actividades para toda la familia, stands informativos y la oportunidad de adoptar a tu nuevo mejor amigo.',
      time: '10:00 - 18:00',
      location: 'Parque Forestal, Santiago',
      cost: 'Gratuito'
    },
    {
      date: '22 Septiembre',
      title: 'Taller "Primeros Auxilios para Mascotas"',
      description: 'Aprende técnicas básicas de primeros auxilios para perros y gatos. Impartido por veterinarios especializados. Incluye práctica con maniquíes y material didáctico.',
      time: '14:00 - 17:00',
      location: 'Centro Veterinario PataRescata',
      cost: '$15.000'
    },
    {
      date: '29 Septiembre',
      title: 'Caminata "Paseo con tu Mascota"',
      description: 'Únete a nuestra caminata mensual por el Parque Metropolitano. Una oportunidad para que tu mascota socialice y haga ejercicio mientras conoces a otros amantes de los animales.',
      time: '09:00 - 12:00',
      location: 'Parque Metropolitano',
      cost: 'Gratuito'
    }
  ];

  // Datos para próximos eventos
  const upcomingEvents = [
    {
      date: '6 Octubre',
      title: 'Clínica Veterinaria Gratuita',
      location: 'Plaza de Armas, Santiago'
    },
    {
      date: '13 Octubre',
      title: 'Concurso de Disfraces para Mascotas',
      location: 'Mall Costanera Center'
    },
    {
      date: '20 Octubre',
      title: 'Charla "Comportamiento Canino"',
      location: 'Biblioteca de Santiago'
    }
  ];

  return (
    <div className="eventos-container">
      {/* Header de la Página */}
      <div className="page-header">
        <h1 className="page-title">Eventos</h1>
        <p className="page-subtitle">
          Descubre todos los eventos relacionados con mascotas en tu área. 
          Desde adopciones hasta talleres educativos, hay algo para todos.
        </p>
      </div>

      {/* Calendario de Eventos */}
      <div className="calendar-section">
        <h2 className="section-title">Calendario de Eventos</h2>
        <div className="calendar-header">
          <div className="calendar-nav">
            <button onClick={previousMonth}>
              <i className="fas fa-chevron-left"></i>
            </button>
            <span className="current-month">{monthNames[currentMonth]} {currentYear}</span>
            <button onClick={nextMonth}>
              <i className="fas fa-chevron-right"></i>
            </button>
          </div>
          <button onClick={goToToday} className="btn btn-primary">
            <i className="fas fa-calendar-day"></i> Hoy
          </button>
        </div>
        <div className="calendar-grid">
          {renderCalendar()}
        </div>
      </div>

      {/* Eventos Destacados */}
      <div className="events-section">
        <h2 className="section-title">Eventos Destacados</h2>
        <div className="events-grid">
          {featuredEvents.map((event, index) => (
            <div className="event-card" key={index}>
              <div className="event-date">{event.date}</div>
              <h3 className="event-title">{event.title}</h3>
              <p className="event-description">{event.description}</p>
              <div className="event-details">
                <div className="event-detail">
                  <i className="fas fa-clock"></i>
                  <span>{event.time}</span>
                </div>
                <div className="event-detail">
                  <i className="fas fa-map-marker-alt"></i>
                  <span>{event.location}</span>
                </div>
                <div className="event-detail">
                  <i className="fas fa-users"></i>
                  <span>{event.cost}</span>
                </div>
              </div>
              <div className="event-actions">
                <a href="#" className="btn btn-primary">
                  <i className="fas fa-calendar-plus"></i> Agregar al Calendario
                </a>
                <a href="#" className="btn btn-secondary">
                  <i className="fas fa-info-circle"></i> Más Información
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Próximos Eventos */}
      <div className="upcoming-events">
        <h3>Próximos Eventos</h3>
        <div className="upcoming-list">
          {upcomingEvents.map((event, index) => (
            <div className="upcoming-item" key={index}>
              <div className="upcoming-date">{event.date}</div>
              <h4 className="upcoming-title">{event.title}</h4>
              <p className="upcoming-location">{event.location}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Sección CTA */}
      <div className="cta-section">
        <h3 className="cta-title">¿Quieres Organizar un Evento?</h3>
        <p className="cta-description">
          Si tienes una idea para un evento relacionado con mascotas, 
          ¡nos encantaría ayudarte a organizarlo! Contáctanos para más información.
        </p>
        <div className="cta-buttons">
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

export default Eventos;
