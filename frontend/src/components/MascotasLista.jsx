import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './MascotasLista.css';

const MascotasLista = () => {
  const [mascotas, setMascotas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Filtros
  const [filtros, setFiltros] = useState({
    especie: '',
    sexo: '',
    edad: '',
    tamanio: '',
    ubicacion: ''
  });

  useEffect(() => {
    // Simulación de carga de mascotas desde API
    const fetchMascotas = async () => {
      try {
        // Aquí se haría la llamada real a la API
        // const response = await fetch('/api/mascotas');
        // const data = await response.json();
        
        // Por ahora simulamos datos
        const data = [
          {
            id: 1,
            nombre: 'Luna',
            imagen: '/static/images/dog1.jpg',
            especie: 'Perro',
            raza: 'Mestizo',
            edad: '2 años',
            sexo: 'Hembra',
            tamanio: 'Mediano',
            ubicacion: 'Santiago',
            descripcion: 'Luna es una perrita muy cariñosa y juguetona que busca un hogar amoroso.',
            disponible: true,
            fundacion: 'Patitas Felices'
          },
          {
            id: 2,
            nombre: 'Simba',
            imagen: '/static/images/dog2.jpg',
            especie: 'Perro',
            raza: 'Golden Retriever',
            edad: '3 años',
            sexo: 'Macho',
            tamanio: 'Grande',
            ubicacion: 'Viña del Mar',
            descripcion: 'Simba es un perro activo y amigable que adora jugar y correr al aire libre.',
            disponible: true,
            fundacion: 'Rescate Animal'
          },
          {
            id: 3,
            nombre: 'Mia',
            imagen: '/static/images/cat1.jpg',
            especie: 'Gato',
            raza: 'Siamés',
            edad: '1 año',
            sexo: 'Hembra',
            tamanio: 'Pequeño',
            ubicacion: 'Concepción',
            descripcion: 'Mia es una gatita tranquila y cariñosa que busca un hogar tranquilo.',
            disponible: true,
            fundacion: 'Gatitos Felices'
          },
          {
            id: 4,
            nombre: 'Rocky',
            imagen: '/static/images/dog3.jpg',
            especie: 'Perro',
            raza: 'Pastor Alemán',
            edad: '4 años',
            sexo: 'Macho',
            tamanio: 'Grande',
            ubicacion: 'Santiago',
            descripcion: 'Rocky es un perro grande y protector, ideal para familias con niños.',
            disponible: false,
            fundacion: 'Rescate Animal'
          },
          {
            id: 5,
            nombre: 'Pelusa',
            imagen: '/static/images/cat2.jpg',
            especie: 'Gato',
            raza: 'Persa',
            edad: '2 años',
            sexo: 'Hembra',
            tamanio: 'Pequeño',
            ubicacion: 'Valparaíso',
            descripcion: 'Pelusa es una gatita muy juguetona y cariñosa que adora ser el centro de atención.',
            disponible: true,
            fundacion: 'Patitas Felices'
          },
          {
            id: 6,
            nombre: 'Max',
            imagen: '/static/images/dog4.jpg',
            especie: 'Perro',
            raza: 'Bulldog',
            edad: '5 años',
            sexo: 'Macho',
            tamanio: 'Mediano',
            ubicacion: 'Santiago',
            descripcion: 'Max es un perro tranquilo y amigable que busca una familia que le dé mucho amor.',
            disponible: true,
            fundacion: 'Patitas Felices'
          }
        ];
        
        setMascotas(data);
        setLoading(false);
      } catch (err) {
        setError('Error al cargar las mascotas');
        setLoading(false);
        console.error(err);
      }
    };

    fetchMascotas();
  }, []);

  // Manejar cambios en los filtros
  const handleFiltroChange = (e) => {
    const { name, value } = e.target;
    setFiltros(prevFiltros => ({
      ...prevFiltros,
      [name]: value
    }));
  };

  // Aplicar filtros a las mascotas
  const mascotasFiltradas = mascotas.filter(mascota => {
    return (
      (filtros.especie === '' || mascota.especie === filtros.especie) &&
      (filtros.sexo === '' || mascota.sexo === filtros.sexo) &&
      (filtros.edad === '' || mascota.edad.includes(filtros.edad)) &&
      (filtros.tamanio === '' || mascota.tamanio === filtros.tamanio) &&
      (filtros.ubicacion === '' || mascota.ubicacion === filtros.ubicacion)
    );
  });

  // Resetear filtros
  const resetFiltros = () => {
    setFiltros({
      especie: '',
      sexo: '',
      edad: '',
      tamanio: '',
      ubicacion: ''
    });
  };

  return (
    <div className="mascotas-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Encuentra a tu compañero ideal</h1>
          <p className="hero-subtitle">
            Explora nuestra lista de mascotas en adopción y encuentra a tu compañero perfecto.
            Todas estas mascotas están buscando un hogar lleno de amor y cuidado.
          </p>
        </div>
      </section>

      {/* Contenido Principal */}
      <div className="main-content">
        <h2 className="section-title">Mascotas en Adopción</h2>

        {/* Sección de Filtros */}
        <section className="filters-section">
          <div className="filters-title">
            <i className="fas fa-filter"></i> Filtrar Mascotas
          </div>
          <div className="filters-grid">
            <div className="filter-group">
              <label className="filter-label" htmlFor="especie">Especie</label>
              <select 
                id="especie" 
                name="especie" 
                className="filter-select"
                value={filtros.especie}
                onChange={handleFiltroChange}
              >
                <option value="">Todas</option>
                <option value="Perro">Perros</option>
                <option value="Gato">Gatos</option>
              </select>
            </div>

            <div className="filter-group">
              <label className="filter-label" htmlFor="sexo">Sexo</label>
              <select 
                id="sexo" 
                name="sexo" 
                className="filter-select"
                value={filtros.sexo}
                onChange={handleFiltroChange}
              >
                <option value="">Todos</option>
                <option value="Macho">Macho</option>
                <option value="Hembra">Hembra</option>
              </select>
            </div>

            <div className="filter-group">
              <label className="filter-label" htmlFor="edad">Edad</label>
              <select 
                id="edad" 
                name="edad" 
                className="filter-select"
                value={filtros.edad}
                onChange={handleFiltroChange}
              >
                <option value="">Todas</option>
                <option value="cachorro">Cachorros</option>
                <option value="joven">Jóvenes</option>
                <option value="adulto">Adultos</option>
                <option value="senior">Adultos mayores</option>
              </select>
            </div>

            <div className="filter-group">
              <label className="filter-label" htmlFor="tamanio">Tamaño</label>
              <select 
                id="tamanio" 
                name="tamanio" 
                className="filter-select"
                value={filtros.tamanio}
                onChange={handleFiltroChange}
              >
                <option value="">Todos</option>
                <option value="Pequeño">Pequeño</option>
                <option value="Mediano">Mediano</option>
                <option value="Grande">Grande</option>
              </select>
            </div>

            <div className="filter-group">
              <label className="filter-label" htmlFor="ubicacion">Ubicación</label>
              <select 
                id="ubicacion" 
                name="ubicacion" 
                className="filter-select"
                value={filtros.ubicacion}
                onChange={handleFiltroChange}
              >
                <option value="">Todas</option>
                <option value="Santiago">Santiago</option>
                <option value="Viña del Mar">Viña del Mar</option>
                <option value="Concepción">Concepción</option>
                <option value="Valparaíso">Valparaíso</option>
              </select>
            </div>

            <div className="filter-group filter-buttons">
              <button className="filter-btn" onClick={resetFiltros}>
                <i className="fas fa-sync-alt"></i> Resetear Filtros
              </button>
            </div>
          </div>
        </section>

        {/* Grilla de Mascotas */}
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Cargando mascotas...</p>
          </div>
        ) : error ? (
          <div className="error-container">
            <i className="fas fa-exclamation-triangle"></i>
            <p>{error}</p>
          </div>
        ) : (
          <>
            <div className="resultados-info">
              Se encontraron {mascotasFiltradas.length} mascotas
            </div>
            
            <div className="pets-grid">
              {mascotasFiltradas.length > 0 ? (
                mascotasFiltradas.map(mascota => (
                  <div className="pet-card" key={mascota.id}>
                    <div className="pet-image-container">
                      <img src={mascota.imagen} alt={mascota.nombre} className="pet-image" />
                      {mascota.disponible ? (
                        <span className="pet-status">Disponible</span>
                      ) : (
                        <span className="pet-status adopted">Adoptado</span>
                      )}
                    </div>
                    <div className="pet-info">
                      <h3 className="pet-name">
                        <i className={mascota.especie === 'Perro' ? 'fas fa-dog' : 'fas fa-cat'}></i>
                        {mascota.nombre}
                      </h3>
                      <div className="pet-details">
                        <div className="pet-detail">
                          <i className="fas fa-paw"></i>
                          <span>{mascota.especie}</span>
                        </div>
                        <div className="pet-detail">
                          <i className="fas fa-venus-mars"></i>
                          <span>{mascota.sexo}</span>
                        </div>
                        <div className="pet-detail">
                          <i className="fas fa-birthday-cake"></i>
                          <span>{mascota.edad}</span>
                        </div>
                        <div className="pet-detail">
                          <i className="fas fa-ruler-vertical"></i>
                          <span>{mascota.tamanio}</span>
                        </div>
                      </div>
                      <p className="pet-description">{mascota.descripcion}</p>
                      <div className="pet-actions">
                        <Link to={`/mascotas/${mascota.id}`} className="action-btn btn-primary">
                          <i className="fas fa-heart"></i> Conocer más
                        </Link>
                      </div>
                      <div className="pet-foundation">
                        <i className="fas fa-home"></i> {mascota.fundacion}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-results">
                  <i className="fas fa-search"></i>
                  <p>No se encontraron mascotas con los filtros seleccionados</p>
                  <button className="reset-btn" onClick={resetFiltros}>
                    Resetear Filtros
                  </button>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default MascotasLista;
