import React from "react";
import { Link } from "react-router-dom";

const Footer = () => {
    return (
        <footer className="bg-light text-center text-muted py-4 mt-5 shadow-sm">
                <div style={{ display: 'flex', gap: '4rem', alignItems: 'center', justifyContent: 'center' }}>
                <p className="mb-2">© 2025 Abogadazo. Todos los derechos reservados.</p>
                <Link to="/Acerca-de" className="text-decoration-none text-dark">Acerca de</Link>
                <Link to="/Contacto" className="text-decoration-none text-dark">Contacto</Link>
                <Link to="/Aviso-legal" className="text-decoration-none text-dark">Aviso Legal</Link>
                <button className="btn btn-sm btn-outline-dark">🌙 Modo Oscuro</button>
            </div>        
        </footer>
    );
}

export default Footer;
