import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

// Componentes comunes
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Páginas públicas
import Home from './components/Home';
import MascotasLista from './components/MascotasLista';
import Blog from './components/Blog';
import Nosotros from './components/Nosotros';
import FAQ from './components/FAQ';
import Eventos from './components/Eventos';

// Componentes de autenticación
import Login from './components/Login';
import AdoptanteRegister from './components/AdoptanteRegister';
import FundacionRegister from './components/FundacionRegister';
import SelectUserType from './components/SelectUserType';
import VerificarCuenta from './components/VerificarCuenta';

// Componente para proteger rutas que requieren autenticación
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem('authToken') !== null;
  
  if (!isAuthenticated) {
    return <Navigate to="/seleccionar-cuenta" />;
  }
  
  return children;
};

// Componente para redireccionar según el tipo de usuario
const UserTypeRoute = ({ children }) => {
  const userType = localStorage.getItem('userType');
  
  if (!userType) {
    return <Navigate to="/seleccionar-cuenta" />;
  }
  
  return children;
};

const AppRouter = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <main className="app-main">
          <Routes>
            {/* Rutas públicas */}
            <Route path="/" element={<Home />} />
            <Route path="/mascotas" element={<MascotasLista />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/nosotros" element={<Nosotros />} />
            <Route path="/faq" element={<FAQ />} />
            <Route path="/eventos" element={<Eventos />} />
            
            {/* Rutas de autenticación */}
            <Route path="/seleccionar-cuenta" element={<SelectUserType />} />
            <Route path="/login/adoptante" element={<Login userType="adoptante" />} />
            <Route path="/login/fundacion" element={<Login userType="fundacion" />} />
            <Route path="/registro/adoptante" element={<AdoptanteRegister />} />
            <Route path="/registro/fundacion" element={<FundacionRegister />} />
            <Route path="/verificar-cuenta/:token" element={<VerificarCuenta />} />
            
            {/* Rutas protegidas para cualquier usuario autenticado */}
            <Route 
              path="/perfil" 
              element={
                <ProtectedRoute>
                  <div>Perfil de Usuario</div>
                </ProtectedRoute>
              } 
            />
            
            {/* Rutas específicas para adoptantes */}
            <Route 
              path="/perfil-adoptante" 
              element={
                <ProtectedRoute>
                  <UserTypeRoute>
                    <div>Perfil de Adoptante</div>
                  </UserTypeRoute>
                </ProtectedRoute>
              } 
            />
            
            {/* Rutas específicas para fundaciones */}
            <Route 
              path="/perfil-fundacion" 
              element={
                <ProtectedRoute>
                  <UserTypeRoute>
                    <div>Perfil de Fundación</div>
                  </UserTypeRoute>
                </ProtectedRoute>
              } 
            />
            
            {/* Ruta para manejar rutas no encontradas */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
        <Footer />
      </BrowserRouter>
    </AuthProvider>
  );
};

export default AppRouter;
