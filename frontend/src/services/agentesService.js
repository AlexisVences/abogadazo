export async function consultarAgente(placa,id_usuario) {
  try {
    const response = await fetch(`https://3568-2806-106e-1e-8e41-a5ce-2334-d890-509d.ngrok-free.app/api/agentes/consulta?placa=${placa}&id=${id_usuario}`,{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "1"
      }
    });
    if (!response.ok) {
      throw new Error('El agente no está registrado en la Gaceta Oficial, puedes impugnar la multa ante el Tribunal de Justicia Administrativa de la CDMX.');
    }
    return await response.json();
  } catch (error) {
    console.error("Error al consultar agente:", error);
    throw error;
  }
}