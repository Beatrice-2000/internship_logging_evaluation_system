import axios from 'axios';

const API = axios.create({
  baseURL: 'https://iles-backend-sdd4.onrender.com/',
});

// Attach access token to every request
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auto-refresh token on 401 errors
API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;

    // If 401 and we haven't already retried
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        const refresh = localStorage.getItem('refresh');
        const res = await axios.post('http://localhost:8000/api/token/refresh/', {
          refresh,
        });
        const newAccess = res.data.access;
        localStorage.setItem('token', newAccess);
        original.headers.Authorization = `Bearer ${newAccess}`;
        return API(original); // retry the original request
      } catch (refreshError) {
        // Refresh token also expired — force logout
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default API;