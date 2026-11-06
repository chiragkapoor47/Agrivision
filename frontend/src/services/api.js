/**
 * TAH-015: Frontend API Service Client
 * Handles HTTP requests, JWT token header injection, and response parsing.
 */

const API_BASE = '/api';

function getAuthHeader() {
  const token = localStorage.getItem('agri_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request(endpoint, options = {}) {
  const headers = {
    ...getAuthHeader(),
    ...(options.headers || {})
  };

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  });

  if (!response.ok) {
    let errorDetail = `Request failed with status ${response.status}`;
    try {
      const errJson = await response.json();
      errorDetail = errJson.detail || errorDetail;
    } catch (e) {
      // Non-json error
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export const authApi = {
  login: (credentials) => request('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  }),
  register: (userData) => request('/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  }),
  getMe: () => request('/auth/me'),
  updateProfile: (profileData) => request('/auth/profile', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profileData)
  })
};

export const predictApi = {
  predictLeaf: (formData) => {
    // Note: Do not set Content-Type header manually for multipart/form-data so browser sets boundary
    const headers = { ...getAuthHeader() };
    return fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers,
      body: formData
    }).then(async (res) => {
      if (!res.ok) {
        let errText = `Scan failed with status ${res.status}`;
        try {
          const err = await res.json();
          errText = err.detail || errText;
        } catch (_) {}
        throw new Error(errText);
      }
      return res.json();
    });
  }
};

export const diagnosisApi = {
  getHistory: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/diagnosis/history${query ? `?${query}` : ''}`);
  },
  getDetail: (id) => request(`/diagnosis/${id}`),
  deleteRecord: (id) => request(`/diagnosis/${id}`, { method: 'DELETE' })
};

export const agriApi = {
  getCrops: () => request('/crops'),
  getDiseases: () => request('/diseases'),
  getTreatments: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/treatments${query ? `?${query}` : ''}`);
  },
  getWeather: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/weather${query ? `?${query}` : ''}`);
  }
};

export const dashboardApi = {
  getStats: () => request('/dashboard/stats')
};

export const resourcesApi = {
  getResources: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/resources${query ? `?${query}` : ''}`);
  }
};
