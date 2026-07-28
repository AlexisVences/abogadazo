import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import VerMas from '../components/VerMas';
import home from '../assets/home.png'
import infraccionimage from '../assets/infraccion.png'

const Home = () => {
    return (
    <>
        <Navbar />
        <div    
            style={{
                backgroundImage: `url(${home})`,
                height: "100vh",
                backgroundSize: "cover",
                backgroundPosition: "center",
                backgroundRepeat: "no-repeat",
                // marginTop: "10px"
            }}
            >
        </div>
        <main className="container mt-5">
            <div className="container text-center my-5">
                <h1 className="display-4">Bienvenido a Abogadazo</h1>
                <p className="lead">
                    Tu asistente legal inteligente para casos de tránsito en la Ciudad de México.
                </p>
                <p>
                    Inicia sesión para comenzar o explorar nuestros servicios.
                </p>
            </div>

            <section className="mt-5">
            <h2 className="mb-4">¿Qué ofrecemos?</h2>
            <div className="row">
                <VerMas
                title="Asesoría Legal Gratuita"
                description="Recibe orientación de una inteligencia artificial que se basa en los documentos legales de tránsito."
                />
                <VerMas
                title="Consulta de Multas y Sanciones"
                description="Accede a información sobre infracciones, puntos en tu licencia y cómo impugnar una multa."
                />
                <VerMas
                title="Guías y Recursos Legales"
                description="Aprende sobre el reglamento de tránsito, tipos de infracciones, seguros y procedimientos legales."
                />
                <VerMas
                title="Consultar Agentes Facultados para Infraccionar"
                description="Te informamos si un oficial está facultado para infraccionarte mediante su número de placa."
                />
            </div>
            </section>

            <section className="mt-5">
                <div className="row align-items-center">
                    {/* Columna del texto */}
                    <div className="col-md-6">
                    <h2 className="mb-3">¿Quiénes somos?</h2>
                    <p>
                        Desarrollado por estudiantes de la Escuela Superior de Cómputo del Instituto Politéncico Nacional, Abogadazo es una herramienta desarrollada con el objetivo de brindar 
                        asesoría legal en materia de tránsito en la Ciudad de México. Somos un equipo comprometido 
                        con facilitar el acceso a la información pública para todos y la justicia por igual,
                        la presente página utiliza inteligencia artificial para facilitar la comprensión de los reglamentos, artículos, 
                        sanciones, procedimientos y derechos ciudadanos relacionados con el tránsito vehicular.
                    </p>
                    <p>
                        Nuestra misión es apoyar a los ciudadanos en la defensa de sus derechos viales, 
                        poniendo a su alcance una plataforma fácil de usar, confiable y sustentada únicamente en documentos legales oficiales
                        procesados con inteligencia artificial.
                    </p>
                    </div>

                    {/* Columna de la imagen */}
                    <div className="col-md-6 text-center">
                    <img
                        src={infraccionimage}
                        alt="Ilustración sobre Abogadazo"
                        style={{
                        maxWidth: '90%',
                        height: 'auto',
                        borderRadius: '12px',
                        boxShadow: '0 0 10px rgba(0,0,0,0.15)',
                        }}
                    />
                    </div>
                </div>
            </section>

            <section className="container mt-5 mb-5">
                <div className="alert alert-secondary" role="alert">
                    <p className="mb-2">
                    <strong>Descargo de responsabilidad:</strong> La información proporcionada por esta plataforma tiene como objetivo brindar orientación basada exclusivamente en los documentos legales emitidos por el Gobierno de la Ciudad de México en materia de tránsito vehicular. Esta herramienta está diseñada como un apoyo informativo y de consulta, y en ningún caso sustituye el asesoramiento legal profesional o la intervención de autoridades competentes.
                    </p>
                    <hr />
                    <p className="fw-semibold mb-2">Documentos legales referentes al tránsito vehicular en la Ciudad de México:</p>
                    <ul className="mb-0">
                    <li><a href="https://data.consejeria.cdmx.gob.mx/images/leyes/reglamentos/REGLAMENTO_DE_TRANSITO_DE_LA_CIUDAD_DE_MEXICO_6.1.pdf" target="_blank" rel="noopener noreferrer">Reglamento de Tránsito de la CDMX</a></li>
                    <li><a href="https://data.consejeria.cdmx.gob.mx/images/leyes/leyes/LEY_DE_MOVILIDAD_DE_LA_CDMX_3.2.pdf" target="_blank" rel="noopener noreferrer">Ley de Movilidad de la CDMX</a></li>
                    <li><a href="https://www.congresocdmx.gob.mx/media/documentos/49a0a80ee030f12d0f797c671da2918e508f30cb.pdf" target="_blank" rel="noopener noreferrer">Ley de cultura cívica en la CDMX</a></li>
                    <li><a href="https://data.consejeria.cdmx.gob.mx/images/leyes/leyes/LEY_DE_PROCEDIMIENTO_ADMINISTRATIVO_DE_LA_CDMX_1.1.pdf" target="_blank" rel="noopener noreferrer">Ley de procedimiento administrativo en la CDMX</a></li>
                    <li><a href="https://www.ssc.cdmx.gob.mx/storage/app/media/Transito/Actualizaciones/Acuedo-40-2024.pdf" target="_blank" rel="noopener noreferrer">Lista de agentes facultados para ifnraccionar sobre vía pública en la CDMX</a></li>

                    </ul>
                </div>
            </section>

        </main>
        <Footer />
        </>
    );
    };

export default Home;
