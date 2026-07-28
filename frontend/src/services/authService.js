// src/services/authService.js
import axios from 'axios';

const API_URL = 'https://abogadazo-back.onrender.com/usuarios';

const login = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/login`, {
      usuario: credentials.username,
      password: credentials.password
    });
    
    const userData = {
      id: response.data.usuario.id,
      nombre: response.data.usuario.nombre,
      apellido: response.data.usuario.apellido,
      correo: response.data.usuario.email,
      rol: response.data.usuario.rol
      // Agrega otros campos necesarios
    };

    // Si el backend devuelve un token en el objeto usuario, guárdalo
    if (response.data.usuario.token) {
      localStorage.setItem('token', response.data.usuario.token);
    }

    localStorage.setItem('user', JSON.stringify(userData));

    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Credenciales incorrectas');
  }
};

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem('user'));
};

export default {
  login,
  logout,
  getCurrentUser
};