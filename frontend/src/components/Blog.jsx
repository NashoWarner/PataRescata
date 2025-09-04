import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Blog.css';

const Blog = () => {
  const [articulos, setArticulos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    // Simulación de carga de artículos del blog desde API
    const fetchArticulos = async () => {
      try {
        // Aquí se haría la llamada real a la API
        // const response = await fetch('/api/blog/articulos');
        // const data = await response.json();
        
        // Por ahora simulamos datos
        const data = [
          {
            id: 1,
            titulo: 'Consejos para la adaptación de tu mascota adoptada',
            imagen: '/static/images/adoption-tips.jpg',
            resumen: 'Aprende cómo ayudar a tu nueva mascota a adaptarse a su hogar después de la adopción. Consejos prácticos que harán la transición más fácil tanto para ti como para tu nuevo compañero.',
            fecha: '15 de mayo, 2023',
            autor: 'María González',
            destacado: true
          },
          {
            id: 2,
            titulo: 'Los beneficios de adoptar una mascota adulta',
            imagen: '/static/images/adult-pet.jpg',
            resumen: 'Descubre por qué adoptar una mascota adulta puede ser la mejor decisión para muchas familias. Conoce sus ventajas y desafíos específicos.',
            fecha: '3 de junio, 2023',
            autor: 'Carlos Martínez'
          },
          {
            id: 3,
            titulo: 'Cuidados especiales para mascotas rescatadas con traumas',
            imagen: '/static/images/rescued-pet.jpg',
            resumen: 'Muchas mascotas rescatadas vienen con traumas del pasado. Aprende técnicas y estrategias para ayudarles a superar sus miedos y traumas.',
            fecha: '22 de junio, 2023',
            autor: 'Ana Silva'
          },
          {
            id: 4,
            titulo: 'Preparando tu hogar para recibir a una mascota',
            imagen: '/static/images/home-prep.jpg',
            resumen: 'Guía completa para preparar tu hogar antes de la llegada de tu nueva mascota. Desde protección de cables hasta juguetes necesarios.',
            fecha: '7 de julio, 2023',
            autor: 'Jorge Pérez'
          },
          {
            id: 5,
            titulo: 'El proceso de socialización en cachorros adoptados',
            imagen: '/static/images/puppy-socialization.jpg',
            resumen: 'La socialización temprana es clave para un desarrollo saludable. Conoce las mejores prácticas para socializar a tu cachorro adoptado.',
            fecha: '19 de julio, 2023',
            autor: 'Laura Sánchez'
          }
        ];
        
        setArticulos(data);
        setLoading(false);
      } catch (err) {
        setError('Error al cargar los artículos del blog');
        setLoading(false);
        console.error(err);
      }
    };

    fetchArticulos();
  }, []);

  // Separar el artículo destacado del resto
  const articuloDestacado = articulos.find(articulo => articulo.destacado);
  const articulosRegulares = articulos.filter(articulo => !articulo.destacado);

  return (
    <div className="blog-container">
      {/* Hero Section del Blog */}
      <section className="blog-hero">
        <div className="blog-hero-content">
          <h1 className="blog-title">Blog PataRescata</h1>
          <p className="blog-subtitle">
            Consejos, historias y recursos para amantes de los animales.
            Aprende sobre cuidados, entrenamiento y más para darle a tu mascota la mejor vida posible.
          </p>
        </div>
      </section>

      {/* Contenido Principal */}
      <div className="main-content">
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Cargando artículos...</p>
          </div>
        ) : error ? (
          <div className="error-container">
            <i className="fas fa-exclamation-triangle"></i>
            <p>{error}</p>
          </div>
        ) : (
          <div className="blog-grid">
            {/* Artículo Destacado */}
            {articuloDestacado && (
              <div className="featured-article">
                <div className="featured-image">
                  <img src={articuloDestacado.imagen} alt={articuloDestacado.titulo} />
                </div>
                <div className="featured-content">
                  <h2 className="featured-title">{articuloDestacado.titulo}</h2>
                  <p className="featured-date">
                    <i className="far fa-calendar-alt"></i> {articuloDestacado.fecha} | 
                    <i className="far fa-user"></i> {articuloDestacado.autor}
                  </p>
                  <p className="featured-summary">{articuloDestacado.resumen}</p>
                  <Link to={`/blog/${articuloDestacado.id}`} className="read-button">
                    Leer artículo
                  </Link>
                </div>
              </div>
            )}

            {/* Artículos Regulares */}
            {articulosRegulares.map(articulo => (
              <div className="article-card" key={articulo.id}>
                <div className="article-image">
                  <img src={articulo.imagen} alt={articulo.titulo} />
                </div>
                <div className="article-content">
                  <h3 className="article-title">{articulo.titulo}</h3>
                  <p className="article-date">
                    <i className="far fa-calendar-alt"></i> {articulo.fecha} | 
                    <i className="far fa-user"></i> {articulo.autor}
                  </p>
                  <p className="article-summary">{articulo.resumen}</p>
                  <Link to={`/blog/${articulo.id}`} className="article-button">
                    Leer más
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
        
        {/* Suscripción al Newsletter */}
        <div className="newsletter-section">
          <div className="newsletter-content">
            <h2>¡Mantente informado!</h2>
            <p>Suscríbete a nuestro newsletter para recibir los últimos artículos y consejos sobre cuidado animal.</p>
            <form className="newsletter-form">
              <input type="email" placeholder="Tu correo electrónico" required />
              <button type="submit">Suscribirme</button>
            </form>
          </div>
        </div>
        
        {/* Categorías */}
        <div className="categories-section">
          <h3>Categorías</h3>
          <div className="categories-container">
            <Link to="/blog/categoria/cuidados" className="category-tag">Cuidados</Link>
            <Link to="/blog/categoria/adopcion" className="category-tag">Adopción</Link>
            <Link to="/blog/categoria/entrenamiento" className="category-tag">Entrenamiento</Link>
            <Link to="/blog/categoria/nutricion" className="category-tag">Nutrición</Link>
            <Link to="/blog/categoria/historias" className="category-tag">Historias de éxito</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Blog;
