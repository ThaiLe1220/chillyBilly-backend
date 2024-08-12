// ./frontend/my-app/services/api.js

import axios from 'axios';

const API_URL = 'https://face-swap.12pmtech.link/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const createUser = async (userData) => {
  try {
    const response = await api.post('/users/', userData);
    return response.data;
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      throw error.response.data;
    } else if (error.request) {
      // The request was made but no response was received
      throw new Error('No response received from server');
    } else {
      // Something happened in setting up the request that triggered an Error
      throw new Error('Error setting up the request');
    }
  }
};

export const getUsers = () => api.get('/users/');
export const getUser = (id) => api.get(`/users/${id}`);
export const updateUser = (id, userData) => api.put(`/users/${id}`, userData);
export const verifyPassword = (id, password) => api.post(`/users/${id}/verify_password`, { password });
export const deleteUser = (id) => api.delete(`/users/${id}`);
export const createProfile = (id, profileData) => api.post(`/users/${id}/profile/`, profileData);
export const getProfile = (id) => api.get(`/users/${id}/profile/`);
export const updateProfile = (id, profileData) => api.put(`/users/${id}/profile/`, profileData);

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);
export const login = (credentials) => api.post('/login', credentials);



export const createGuest = () => api.post('/guests');
export const getGuests = () => api.get('/guests');
export const getGuest = (id) => api.get(`/guests/${id}`);
export const updateGuest = (id) => api.put(`/guests/${id}`);
export const deleteGuest = (id) => api.delete(`/guests/${id}`);
export const cleanupGuests = () => api.delete('/guests/cleanup/');

export default api;