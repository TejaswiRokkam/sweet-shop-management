const BASE_URL = "https://sweet-shop-management-q36x.onrender.com/api";

export async function apiRequest(endpoint, method = "GET", body) {
  const token = localStorage.getItem("token");

  const headers = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Request failed");
  }

  // Handle 204 No Content (e.g., DELETE)
  if (response.status === 204) {
    return null;
  }

  return response.json();
}
