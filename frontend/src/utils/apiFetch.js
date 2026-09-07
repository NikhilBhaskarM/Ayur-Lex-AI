/**
 * Enhanced fetch wrapper that dynamically attaches JWT Bearer token
 * from localStorage to outgoing HTTP requests.
 */
export async function apiFetch(url, options = {}) {
  const token =
    localStorage.getItem('token') ||
    localStorage.getItem('access_token');

  const headers = new Headers(options.headers || {});

  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('role');
    localStorage.removeItem('user');
  }

  return response;
}

export default apiFetch;
