import React from "react";
import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light px-4 py-3 shadow-sm fixed-top">
            <div className="container">
                <Link className="navbar-brand d-flex align-items-center" to="/BienvenidaAdmin">
                    <img src={logo} alt="Logo" style={{ height: "60px", marginRight: "20px", marginBottom: "0px"}} />
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
                    <br></br>
                    <Link to="/" className="btn btn-dark">Cerrar sesión</Link>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
