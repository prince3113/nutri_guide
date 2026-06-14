const API_BASE = "http://127.0.0.1:5000";

export async function apiRequest(endpoint, options = {}) {
  const token = sessionStorage.getItem("access_token");

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json();

  if (!response.ok) {
    const message =
      data.message ||
      Object.values(data).flat().join(", ") ||
      "Something went wrong";
    throw new Error(message);
  }

  return data;
}

export function setToken(token) {
  sessionStorage.setItem("access_token", token);
}

export function getToken() {
  return sessionStorage.getItem("access_token");
}

export function clearToken() {
  sessionStorage.removeItem("access_token");
}

