const API_URL = (
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1"
).replace(/\/$/, "");

const TOKEN_KEY = "tecapp_access_token";

export class ApiError extends Error {
  constructor(message, status, details = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem(TOKEN_KEY);
}

function saveToken(token, remember) {
  localStorage.removeItem(TOKEN_KEY);
  sessionStorage.removeItem(TOKEN_KEY);
  const storage = remember ? localStorage : sessionStorage;
  storage.setItem(TOKEN_KEY, token);
}

export function clearStoredToken() {
  localStorage.removeItem(TOKEN_KEY);
  sessionStorage.removeItem(TOKEN_KEY);
}

function getErrorMessage(payload, fallback) {
  if (typeof payload?.detail === "string") return payload.detail;

  if (Array.isArray(payload?.detail)) {
    return payload.detail
      .map((item) => item.msg || "Dato inválido")
      .join(". ");
  }

  return fallback;
}

async function request(path, options = {}) {
  const { auth = true, body, headers: customHeaders, ...fetchOptions } = options;
  const headers = new Headers(customHeaders || {});
  headers.set("Accept", "application/json");

  let requestBody = body;
  if (body && !(body instanceof FormData) && !(body instanceof URLSearchParams)) {
    headers.set("Content-Type", "application/json");
    requestBody = JSON.stringify(body);
  }

  if (auth) {
    const token = getStoredToken();
    if (token) headers.set("Authorization", `Bearer ${token}`);
  }

  let response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      ...fetchOptions,
      headers,
      body: requestBody,
    });
  } catch {
    throw new ApiError(
      `No fue posible conectar con el servidor en ${API_URL}.`,
      0,
    );
  }

  const text = await response.text();
  let payload = null;
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch {
      payload = text;
    }
  }

  if (response.status === 401) {
    clearStoredToken();
    window.dispatchEvent(new Event("tecapp:unauthorized"));
  }

  if (!response.ok) {
    throw new ApiError(
      getErrorMessage(payload, `La solicitud falló (${response.status}).`),
      response.status,
      payload,
    );
  }

  return payload;
}

function buildQuery(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      query.set(key, String(value));
    }
  });
  const value = query.toString();
  return value ? `?${value}` : "";
}

export const api = {
  async login(username, password, remember = false) {
    const body = new URLSearchParams({ username, password });
    const data = await request("/token", {
      method: "POST",
      body,
      auth: false,
    });
    saveToken(data.access_token, remember);
    return data;
  },

  registerUser(data) {
    return request("/usuarios/", {
      method: "POST",
      body: data,
      auth: false,
    });
  },

  getProducts(params) {
    return request(`/productos/${buildQuery(params)}`, { auth: false });
  },
  createProduct(data) {
    return request("/productos/", { method: "POST", body: data });
  },
  updateProduct(id, data) {
    return request(`/productos/${id}`, { method: "PUT", body: data });
  },
  deleteProduct(id) {
    return request(`/productos/${id}`, { method: "DELETE" });
  },

  getBrands() {
    return request("/marcas/", { auth: false });
  },
  createBrand(data) {
    return request("/marcas/", { method: "POST", body: data });
  },
  updateBrand(id, data) {
    return request(`/marcas/${id}`, { method: "PATCH", body: data });
  },
  deleteBrand(id) {
    return request(`/marcas/${id}`, { method: "DELETE" });
  },

  getProviders() {
    return request("/proveedores/");
  },
  createProvider(data) {
    return request("/proveedores/", { method: "POST", body: data });
  },
  updateProvider(id, data) {
    return request(`/proveedores/${id}`, { method: "PUT", body: data });
  },
  deleteProvider(id) {
    return request(`/proveedores/${id}`, { method: "DELETE" });
  },

  getUsers() {
    return request("/usuarios/");
  },
  createUser(data) {
    return request("/usuarios/", { method: "POST", body: data });
  },
  updateUser(id, data) {
    return request(`/usuarios/${id}`, { method: "PUT", body: data });
  },
  deleteUser(id) {
    return request(`/usuarios/${id}`, { method: "DELETE" });
  },

  askChatbot(question ) {
    return request("/productos/chat/", {
      method: "POST",
      body: { question },
    });
  },
};

export { API_URL };
