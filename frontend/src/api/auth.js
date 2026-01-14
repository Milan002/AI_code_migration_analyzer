/**
 * Authentication API client
 */

const API_BASE_URL = '/api/auth';

// Token management
export const setToken = (token) => {
  localStorage.setItem('authToken', token);
};

export const getToken = () => {
  return localStorage.getItem('authToken');
};

export const removeToken = () => {
  localStorage.removeItem('authToken');
};

export const isAuthenticated = () => {
  return !!getToken();
};

// Get auth headers for protected requests
export const getAuthHeaders = () => {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};

/**
 * Register a new user
 */
export async function registerUser(email, username, password) {
  const response = await fetch(`${API_BASE_URL}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, username, password }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Registration failed');
  }

  return data;
}

/**
 * Login user and store token
 */
export async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Login failed');
  }

  // Store the token
  setToken(data.access_token);
  return data;
}

/**
 * Logout user
 */
export function logoutUser() {
  removeToken();
}

/**
 * Get current user info
 */
export async function getCurrentUser() {
  const response = await fetch(`${API_BASE_URL}/me`, {
    headers: {
      ...getAuthHeaders(),
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      removeToken();
      throw new Error('Session expired');
    }
    throw new Error('Failed to get user info');
  }

  return response.json();
}
