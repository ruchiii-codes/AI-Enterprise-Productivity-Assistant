/**
 * Environment configuration.
 *
 * Every environment value is read here once. Previously the API base URL was
 * re-declared in eight separate files, so changing it meant eight edits and a
 * missed one failed silently at runtime.
 */

const DEFAULT_API_BASE_URL = "http://localhost:8000";

function readApiBaseUrl() {
  const configured = import.meta.env.VITE_API_BASE_URL;

  if (!configured) {
    // Local development is the only case where falling back is reasonable.
    if (import.meta.env.PROD) {
      console.warn(
        "VITE_API_BASE_URL is not set. Falling back to " +
          `${DEFAULT_API_BASE_URL}, which will not work in production.`
      );
    }

    return DEFAULT_API_BASE_URL;
  }

  // A trailing slash would produce "//chat" once paths are appended.
  return configured.replace(/\/+$/, "");
}

export const API_BASE_URL = readApiBaseUrl();

export const TOKEN_STORAGE_KEY = "access_token";
export const CONVERSATION_STORAGE_KEY = "workmind_conversation_id";
export const THEME_STORAGE_KEY = "workmind_theme";
