import React, { useEffect, useState, useRef } from "react";
import { useLocation } from "react-router-dom";
import NavBar2 from "../components/NavBar2";
import Footer from "../components/Footer";
import "../styles/AsesoriaIA.css";
import { FaPaperPlane, FaStar } from "react-icons/fa";
import { consultarChatLegal, enviarFeedbackLegal } from "../services/legalService";
import authService from "../services/authService";

const AsesoriaIA = () => {
    const location = useLocation();
    const storedUser = authService.getCurrentUser();
    const userId = storedUser?.id;
    const chatEndRef = useRef(null);

    useEffect(() => {
        window.scrollTo(0, 0);
    }, [location]);

    const [consulta, setConsulta] = useState("");
    const [historial, setHistorial] = useState([]);
    const [hoveredRating, setHoveredRating] = useState({});
    const [selectedRatings, setSelectedRatings] = useState({}); 

    useEffect(() => {
    if (chatEndRef.current) {
        chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
    }, [historial]);

    const manejarEnvio = async () => {
        if (consulta.trim() === "") return;

        const nuevaEntrada = {
            pregunta: consulta,
            respuesta: "Cargando...",
        };

        setHistorial((prev) => [...prev, nuevaEntrada]); // Coloca la nueva consulta al final
        setConsulta("");

        try {
            const data = await consultarChatLegal(consulta, userId);
            const nuevaRespuesta = {
                pregunta: consulta,
                respuesta: data.respuesta,
                fuentes: data.fuentes,
                id_respuesta: data.id_respuesta //guardar por cada respuesta
            };
            setHistorial((prev) => {
                const actualizado = [...prev];
                actualizado[actualizado.length - 1] = nuevaRespuesta;
                return actualizado;
            });
        } catch (error) {
            const errorRespuesta = {
                pregunta: consulta,
                respuesta: "Ocurrió un error al procesar tu consulta. Intenta nuevamente.",
            };
            setHistorial((prev) => {
                const actualizado = [...prev];
                actualizado[actualizado.length - 1] = errorRespuesta;
                return actualizado;
            });
        }
    };

    // envia calificacion al backend
const calificarRespuesta = async (index, rating) => {
    const item = historial[index];
    setSelectedRatings((prev) => ({ ...prev, [index]: rating }));

    try {
        await enviarFeedbackLegal({
            userId,
            pregunta: item.pregunta,
            respuesta: item.id_respuesta,
            rating,
        });
    } catch (error) {
        console.error("Error al enviar calificación:", error);
    }
};

    return (
        <>
            <NavBar2 />
            <div className="page-container">
                <main className="content-wrap">
                    <div className="asesoriaia-container container" style={{ paddingTop: '5rem' }}>
                        <div className="main-content">
                            <div className="text-center mb-5">
                                <h1 className="fw-bold display-5 text-dark">Asesoría Legal Inteligente</h1>
                                <p className="fw-light fs-5 text-muted">
                                    Consulta a nuestro asistente legal inteligente sobre cualquier situación de tránsito.
                                </p>
                            </div>

                            {/* Seccion del chat */}
                            <div className="row">
                                <div className="col-lg-8 mb-4">
                                    <div className="chat-box p-4 rounded-4 shadow-sm bg-light d-flex flex-column">
                                        <div className="chat-historial overflow-auto mb-4" style={{ maxHeight: "400px", overflowY: "auto", scrollBehavior: "smooth", flexGrow: 1}}>
                                            {historial.length === 0 ? (
                                                <p className="text-muted fw-light">Aún no has realizado ninguna consulta.</p>
                                            ) : (
                                                historial.map((item, index) => (
                                                    <div key={index} className="mb-4">
                                                        <div className="text-end">
                                                            <p className="fw-bold text-primary mb-1">Tú:</p>
                                                            <div className="bubble-user">{item.pregunta}</div>
                                                        </div>
                                                        <div className="text-start mt-2">
                                                            <p className="fw-bold text-success mb-1">Abogadazo IA:</p>
                                                            <div className="bubble-ia mb-2">
                                                                {item.respuesta.split('\n').map((linea, i) => (
                                                                    <React.Fragment key={i}>
                                                                        {linea}
                                                                        <br />
                                                                    </React.Fragment>
                                                                ))}
                                                            </div>
                                                            {/* seccion de estrellas para calificar */}
                                                            <div className="d-flex justify-content-end align-items-center mt-2">
                                                                {[1, 2, 3, 4, 5].map((estrella) => (
                                                                    <FaStar
                                                                        key={estrella}
                                                                        size={20}
                                                                        style={{ cursor: "pointer", marginLeft: "4px" }}
                                                                        color={
                                                                            (hoveredRating[index] || selectedRatings[index]) >= estrella
                                                                            ? "#ffc107"
                                                                            : "#e4e5e9"
                                                                        }
                                                                        onMouseEnter={() => setHoveredRating((prev) => ({ ...prev, [index]: estrella }))}
                                                                        onMouseLeave={() => setHoveredRating((prev) => ({ ...prev, [index]: null }))}
                                                                        onClick={() => calificarRespuesta(index, estrella)}
                                                                    />
                                                                ))}
                                                            </div>
                                                        </div>
                                                    </div>
                                                ))
                                            )}
                                            <div ref={chatEndRef} />
                                        </div>

                                        {/* Input para nueva consulta */}
                                        <div className="d-flex">
                                            <input
                                                type="text"
                                                className="form-control me-2 shadow-sm"
                                                placeholder="Escribe tu consulta legal aquí..."
                                                value={consulta}
                                                onChange={(e) => setConsulta(e.target.value)}
                                            />
                                            <button onClick={manejarEnvio} className="btn btn-dark d-flex align-items-center">
                                                <FaPaperPlane className="me-2" />
                                                Enviar
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                {/* Seccion de historial */}
                                <div className="col-lg-4">
                                    <div className="historial-box bg-white p-4 rounded-4 shadow-sm h-100">
                                        <h5 className="fw-bold text-dark mb-3">Historial de consultas</h5>
                                        {historial.length === 0 ? (
                                            <p className="text-muted fw-light">Tu historial aparecerá aquí.</p>
                                        ) : (
                                            <ul className="list-group list-group-flush">
                                                {historial.map((item, index) => (
                                                    <li key={index} className="list-group-item fw-light text-muted">
                                                        {item.pregunta.slice(0, 60)}...
                                                    </li>
                                                ))}
                                            </ul>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
            <Footer />
        </>
    );
};

export default AsesoriaIA;
