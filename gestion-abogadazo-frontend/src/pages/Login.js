// src/pages/LoginPage.jsx
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import authService from "../services/authService";
import logo from "../assets/logo.png";

const LoginPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [id]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await authService.login(formData);
      // Obtener el usuario actual después del login
      const currentUser = authService.getCurrentUser();
      
      // Redirigir según el rol
      if (currentUser && currentUser.rol === 'admin') {
        navigate('/BienvenidaAdmin');
      } else {
        navigate('/Bienvenida');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container d-flex align-items-center justify-content-center vh-100">
      <div className="card p-4 shadow-sm" style={{ maxWidth: "400px", width: "100%" }}>
        <div className="d-flex align-items-center justify-content-left mb-4" style={{ gap: "10px" }}>
          <img src={logo} alt="Logo" style={{ height: "40px" }} />
          <h2 className="m-0">Inicia sesión</h2>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="username" className="form-label">Correo electrónico</label>
            <input 
              type="text" 
              className="form-control" 
              id="username" 
              value={formData.username}
              onChange={handleChange}
              required 
            />
          </div>
          <div className="mb-3">
            <label htmlFor="password" className="form-label">Contraseña</label>
            <input 
              type="password" 
              className="form-control" 
              id="password" 
              value={formData.password}
              onChange={handleChange}
              required 
            />
          </div>

          <div className="form-check mb-3">
            <input type="checkbox" className="form-check-input" id="rememberMe" />
            <label className="form-check-label" htmlFor="rememberMe">
              Mantenerme conectado en este dispositivo
            </label>
          </div>

          <button 
            type="submit" 
            className="btn btn-dark w-100"
            disabled={loading}
          >
            {loading ? 'Cargando...' : 'Iniciar sesión'}
          </button>
        </form>

        <div className="text-center my-3">
          <small className="text-muted">o inicia sesión con</small>
        </div>

        <div className="d-flex justify-content-center mb-3" style={{ gap: "20px" }}>
          <button type="button" className="btn btn-outline-dark rounded-circle p-2" style={{ width: "40px", height: "40px" }}>
            <i className="bi bi-apple"></i>
          </button>
          <button type="button" className="btn btn-outline-dark rounded-circle p-2" style={{ width: "40px", height: "40px" }}>
            <i className="bi bi-facebook"></i>
          </button>
          <button type="button" className="btn btn-outline-dark rounded-circle p-2" style={{ width: "40px", height: "40px" }}>
            <i className="bi bi-google"></i>
          </button>
        </div>

        <div className="text-center">
          <small>
            ¿Necesitas ayuda?{" "}
            <Link to="/recuperar-password" className="text-decoration-none">Recuperar contraseña</Link>
          </small>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;