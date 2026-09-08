/**
 * Gmail, Calendar and GitHub connection management.
 *
 * These calls were previously nine raw fetch() calls inlined in Tools.jsx,
 * bypassing the service layer entirely.
 */

import { api } from "./client";

const PROVIDERS = ["github", "gmail", "calendar"];

function assertProvider(provider) {
  if (!PROVIDERS.includes(provider)) {
    throw new Error(`Unknown integration provider: ${provider}`);
  }
}

/** @returns {Promise<{connected: boolean, [key: string]: unknown}>} */
export function getIntegrationStatus(provider) {
  assertProvider(provider);

  return api.get(`/auth/${provider}/status`, {
    errorMessage: `Unable to load ${provider} status.`,
  });
}

/**
 * Begin the OAuth flow. The backend responds with the provider's authorization
 * URL, which the caller redirects the browser to.
 */
export function startIntegrationConnect(provider) {
  assertProvider(provider);

  return api.get(`/auth/${provider}/start`, {
    errorMessage: `Unable to start the ${provider} connection.`,
  });
}

export function disconnectIntegration(provider) {
  assertProvider(provider);

  return api.delete(`/auth/${provider}/disconnect`, {
    errorMessage: `Unable to disconnect ${provider}.`,
  });
}

export { PROVIDERS };
