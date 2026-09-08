import { api, clearToken, setToken } from "./client";

export async function loginUser(email, password) {
  // The backend uses OAuth2PasswordRequestForm, so this must be form-encoded
  // and the email is sent as "username".
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  const data = await api.post("/auth/login", body, {
    auth: false,
    errorMessage: "Login failed.",
  });

  if (data?.access_token) {
    setToken(data.access_token);
  }

  return data;
}

export function logoutUser() {
  clearToken();
}

export function getCurrentUser() {
  return api.get("/auth/me", {
    errorMessage: "Unable to load account information.",
  });
}

export function registerUser(username, email, password) {
  return api.post(
    "/auth/register",
    { username, email, password },
    { auth: false, errorMessage: "Registration failed." }
  );
}

export function verifyEmail(token) {
  return api.get(`/auth/verify-email?token=${encodeURIComponent(token)}`, {
    auth: false,
    errorMessage: "Email verification failed.",
  });
}
