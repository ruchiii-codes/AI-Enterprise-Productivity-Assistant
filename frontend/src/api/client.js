/**
 * HTTP client.
 *
 * One place for the base URL, the auth header, error parsing, and the 401
 * response. Every API module goes through `request`.
 *
 * Previously each service repeated the same ten-line error block and each
 * caller had to read the token from localStorage and pass it in by hand. There
 * was also no handling for an expired token: a 401 left the user on a broken
 * page with no way back to login.
 */

import { API_BASE_URL, TOKEN_STORAGE_KEY } from "../config/env";

/** An HTTP error carrying the backend's status and `detail` message. */
export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

/**
 * Called when the server rejects our credentials. AuthContext registers a
 * handler here so a 401 clears auth state and returns the user to login.
 */
let unauthorizedHandler = null;

export function setUnauthorizedHandler(handler) {
  unauthorizedHandler = handler;
}

export function getToken() {
  try {
    return localStorage.getItem(TOKEN_STORAGE_KEY);
  } catch {
    // Private browsing or blocked storage.
    return null;
  }
}

export function setToken(token) {
  try {
    localStorage.setItem(TOKEN_STORAGE_KEY, token);
  } catch {
    // Non-fatal: the session simply will not survive a reload.
  }
}

export function clearToken() {
  try {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
  } catch {
    // Nothing to do.
  }
}

/**
 * Build the request body and matching Content-Type.
 *
 * FormData must NOT get an explicit Content-Type: the browser has to set it
 * itself so the multipart boundary is included. URLSearchParams is used by the
 * login endpoint, which expects form encoding.
 */
function buildBody(body) {
  if (body === undefined || body === null) {
    return { body: undefined, headers: {} };
  }

  if (body instanceof FormData) {
    return { body, headers: {} };
  }

  if (body instanceof URLSearchParams) {
    return {
      body,
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    };
  }

  return {
    body: JSON.stringify(body),
    headers: { "Content-Type": "application/json" },
  };
}

/** Extract the backend's `detail`, falling back to a caller-supplied message. */
async function extractErrorMessage(response, fallback) {
  try {
    const data = await response.json();
    return data.detail || data.message || fallback;
  } catch {
    return fallback;
  }
}

/**
 * Perform an API request.
 *
 * @param {string} path            Path beginning with "/", e.g. "/auth/login"
 * @param {object} [options]
 * @param {string} [options.method]        Defaults to "GET"
 * @param {any}    [options.body]          Object (JSON), FormData, or URLSearchParams
 * @param {boolean}[options.auth]          Attach the bearer token. Default true
 * @param {string} [options.errorMessage]  Fallback message when the body has no detail
 * @returns {Promise<any>} Parsed JSON, or null for an empty response
 */
export async function request(
  path,
  {
    method = "GET",
    body,
    auth = true,
    errorMessage = "Something went wrong.",
    signal,
  } = {}
) {
  const { body: requestBody, headers: bodyHeaders } = buildBody(body);

  const headers = { ...bodyHeaders };

  if (auth) {
    const token = getToken();

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: requestBody,
    signal,
  });

  if (response.status === 401 && auth) {
    // The token is missing, expired, or invalid. Tear down auth state so the
    // app returns to login rather than sitting on a page that cannot load.
    clearToken();

    if (unauthorizedHandler) {
      unauthorizedHandler();
    }

    throw new ApiError(
      await extractErrorMessage(response, "Your session has expired."),
      401
    );
  }

  if (!response.ok) {
    throw new ApiError(
      await extractErrorMessage(response, errorMessage),
      response.status
    );
  }

  if (response.status === 204) {
    return null;
  }

  // Some endpoints return an empty body with a 200.
  const text = await response.text();

  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export const api = {
  get: (path, options) => request(path, { ...options, method: "GET" }),
  post: (path, body, options) =>
    request(path, { ...options, method: "POST", body }),
  put: (path, body, options) =>
    request(path, { ...options, method: "PUT", body }),
  delete: (path, options) => request(path, { ...options, method: "DELETE" }),
};
