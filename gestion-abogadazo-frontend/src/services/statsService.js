const API_URL = 'https://3568-2806-106e-1e-8e41-a5ce-2334-d890-509d.ngrok-free.app';
export const getDailyStats = async () => {
  
  const response = await fetch(API_URL+'/api/admin/stats/daily',{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "1"
      }
    });
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.message || 'Error al obtener estadísticas diarias');
  }
  
  return data;
};

export const getMonthlyStats = async () => {
  const response = await fetch(API_URL+'/api/admin/stats/monthly',{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "1"
      }
    });
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.message || 'Error al obtener estadísticas mensuales');
  }
  
  return data;
};

export const getMonthlyStatsAgents = async () => {
  const response = await fetch(API_URL+'/api/admin/stats/monthlyagents',{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "1"
      }
    });
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.message || 'Error al obtener estadísticas mensuales');
  }
  
  return data;
};

export const getConsultationTypes = async () => {
  const response = await fetch(API_URL+'/api/admin/stats/types',{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "1"
      }
    });
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.message || 'Error al obtener tipos de consulta');
  }
  
  return data;
};

export const getFeedbackStats = async () => {
  const response = await fetch(API_URL+'/api/admin/stats/feedback',{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "1"
      }
    });
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.message || 'Error al obtener estadísticas de feedback');
  }
  
  return data;
};