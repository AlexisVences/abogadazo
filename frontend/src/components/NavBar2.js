// src/components/Navbar.js
import React from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";
import authService from "../services/authService";

const Navbar = () => {
    // const user = authService.getCurrentUser();
    const navigate = useNavigate();

    const handleLogout = () => {
        authService.logout();
        navigate("/"); // Redirige a la página principal
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light px-4 py-3 shadow-sm fixed-top">
        <div className="container">
            <Link className="navbar-brand d-flex align-items-center" to="/Bienvenida">
            <img src={logo} alt="Logo" style={{ height: "60px", marginRight: "20px" }} />
            <span className="fw-semibold fs-4 text-dark">• A b o g a d a z o</span>
            </Link>
            <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            >
            <span className="navbar-toggler-icon"></span>
            </button>

            <div style={{ display: 'flex', gap: '1rem' }}>

                <>
                <Link to="/Gestionar-perfil" className="btn btn-outline-dark">Gestionar perfil</Link>
                <button onClick={handleLogout} className="btn btn-dark">Cerrar sesión</button>
                </>

            </div>
        </div>
        </nav>
    );
};

export default Navbar;
