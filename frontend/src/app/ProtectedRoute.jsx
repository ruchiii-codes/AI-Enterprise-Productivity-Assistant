import { Navigate, useLocation } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

/**
 * Gate for authenticated routes.
 *
 * Previously every route was public: /chat, /settings and the rest rendered
 * for signed-out visitors, fired their requests, and showed a broken shell.
 *
 * The check is on token presence, which is read synchronously, so there is no
 * flash of the login page on reload. A token that turns out to be expired is
 * caught by the API client's 401 handling, which clears auth state and brings
 * the user back here.
 */
export function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    // `from` lets the login page send the user back where they were headed.
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children;
}

export default ProtectedRoute;
