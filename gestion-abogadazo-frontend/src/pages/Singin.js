import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";
import { createUser } from "../services/userService";

const SignUp = () => {
    const [formData, setFormData] = useState({
        usuario: '',
        nombre: '',
        apellido: '',
        email: '',
        password: '',
        rol: 'usuario'
    });
    const [error, setError] = useState('');
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
        
        // Validar que las contraseñas coincidan
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (password !== confirmPassword) {
            setError('Las contraseñas no coinciden');
            return;
        }

        try {
            // Usamos el servicio importado en lugar de fetch directo
            await createUser({
                ...formData,
                usuario: formData.usuario || formData.email
            });

            // Redirigir a la página de login después de crear el usuario
            navigate('/login');
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="container d-flex align-items-center justify-content-center vh-100">
            <div className="card p-3 shadow-sm" style={{ maxWidth: "340px", width: "100%", fontSize: "0.9rem" }}>
                
                {/* Logo y Título */}
                <div className="d-flex align-items-center justify-content-left mb-3" style={{ gap: "8px" }}>
                <img src={logo} alt="Logo Abogadazo" style={{ height: "32px" }} />
                <h4 className="m-0" style={{ fontSize: "1.7rem" }}>Crear cuenta</h4>
                </div>

                {/* Mostrar error si existe */}
                {error && <div className="alert alert-danger">{error}</div>}

                {/* Formulario */}
                <form onSubmit={handleSubmit}>
                <div className="mb-2">
                    <label htmlFor="nombre" className="form-label">Nombre</label>
                    <input 
                        type="text" 
                        className="form-control form-control-sm" 
                        id="nombre" 
                        value={formData.nombre}
                        onChange={handleChange}
                        required 
                    />
                </div>

                <div className="mb-2">
                    <label htmlFor="apellido" className="form-label">Apellido</label>
                    <input 
                        type="text" 
                        className="form-control form-control-sm" 
                        id="apellido" 
                        value={formData.apellido}
                        onChange={handleChange}
                        required 
                    />
                </div>

                <div className="mb-2">
                    <label htmlFor="email" className="form-label">Correo electrónico</label>
                    <input 
                        type="email" 
                        className="form-control form-control-sm" 
                        id="email" 
                        value={formData.email}
                        onChange={handleChange}
                        required 
                    />
                </div>

                <div className="mb-2">
                    <label htmlFor="password" className="form-label">Contraseña</label>
                    <input 
                        type="password" 
                        className="form-control form-control-sm" 
                        id="password" 
                        value={formData.password}
                        onChange={handleChange}
                        required 
                    />
                </div>

                <div className="mb-3">
                    <label htmlFor="confirmPassword" className="form-label">Confirmar contraseña</label>
                    <input 
                        type="password" 
                        className="form-control form-control-sm" 
                        id="confirmPassword" 
                        required 
                    />
                </div>

                <button type="submit" className="btn btn-dark w-100 btn-sm">Crear cuenta</button>
                </form>

                {/* Divider */}
                <div className="text-center my-2">
                <small className="text-muted">o regístrate con</small>
                </div>

                {/* Botones sociales compactos */}
                <div className="d-flex justify-content-center mb-2" style={{ gap: "16px" }}>
                <button type="button" className="btn btn-outline-dark rounded-circle p-1" style={{ width: "32px", height: "32px", fontSize: "0.85rem" }}>
                    <i className="bi bi-apple"></i>
                </button>
                <button type="button" className="btn btn-outline-dark rounded-circle p-1" style={{ width: "32px", height: "32px", fontSize: "0.85rem" }}>
                    <i className="bi bi-facebook"></i>
                </button>
                <button type="button" className="btn btn-outline-dark rounded-circle p-1" style={{ width: "32px", height: "32px", fontSize: "0.85rem" }}>
                    <i className="bi bi-google"></i>
                </button>
                </div>

                {/* Enlace a login */}
                <div className="text-left mt-2">
                <small className="text-muted">¿Ya tienes cuenta? </small>
                <small className="text-muted">
                    <Link to="/login" className="text-decoration-none">Inicia sesión</Link>
                </small>
                </div>

            </div>
        </div>
    );
};

export default SignUp;