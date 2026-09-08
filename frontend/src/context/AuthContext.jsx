/**
 * Authentication state.
 *
 * Before this, every component read the token from localStorage itself --
 * 22 separate reads across 6 files -- and nothing reacted when the token
 * became invalid. Auth now lives in one place, and the API client reports a
 * 401 straight back here so the session tears down exactly once.
 */

import { useCallback, useEffect, useMemo, useState } from "react";

import {
  getCurrentUser,
  loginUser,
  logoutUser,
} from "../api/auth";
import { getToken, setUnauthorizedHandler } from "../api/client";
import { AuthContext } from "./auth-context";

export function AuthProvider({ children }) {
  // Read synchronously so the first render already knows whether the user is
  // signed in. Deferring this would flash the login page on every reload.
  const [token, setToken] = useState(() => getToken());
  const [user, setUser] = useState(null);
  const [loadingUser, setLoadingUser] = useState(() => Boolean(getToken()));

  const logout = useCallback(() => {
    logoutUser();
    setToken(null);
    setUser(null);
  }, []);

  // The API client calls this when the server rejects our credentials.
  useEffect(() => {
    setUnauthorizedHandler(() => {
      // The client has already cleared storage; just drop the in-memory state.
      setToken(null);
      setUser(null);
    });

    return () => setUnauthorizedHandler(null);
  }, []);

  useEffect(() => {
    let active = true;

    const loadUser = async () => {
      if (!token) {
        if (active) {
          setUser(null);
          setLoadingUser(false);
        }
        return;
      }

      try {
        const profile = await getCurrentUser();

        if (active) {
          setUser(profile);
        }
      } catch {
        // A 401 has already been handled by the client's handler above.
        if (active) {
          setUser(null);
        }
      } finally {
        if (active) {
          setLoadingUser(false);
        }
      }
    };

    loadUser();

    return () => {
      active = false;
    };
  }, [token]);

  const login = useCallback(async (email, password) => {
    // loginUser persists the token; mirror it into state so consumers re-render.
    const data = await loginUser(email, password);

    setToken(data.access_token);

    return data;
  }, []);

  const value = useMemo(
    () => ({
      token,
      user,
      loadingUser,
      isAuthenticated: Boolean(token),
      login,
      logout,
    }),
    [token, user, loadingUser, login, logout]
  );

  return (
    <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
  );
}
