import { useNavigate } from "react-router-dom";

import Brand from "../components/ui/Brand";
import { useAuth } from "../hooks/useAuth";
import "../styles/auth.css";

/**
 * Real 404.
 *
 * The wildcard route used to redirect to /login, so a mistyped URL silently
 * signed you out of a working session.
 */
function NotFound() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const destination = isAuthenticated ? "/workspace" : "/login";
  const label = isAuthenticated ? "Back to workspace" : "Go to sign in";

  return (
    <main className="auth-page">
      <section className="auth-shell">
        <div className="auth-form-panel">
          <div className="auth-form-container">
            <div className="mobile-brand">
              <Brand compact />
            </div>

            <div className="form-heading">
              <span className="form-kicker">404</span>

              <h2>Page not found</h2>

              <p>
                That page does not exist. It may have moved, or the link may
                be out of date.
              </p>
            </div>

            <button
              type="button"
              className="auth-submit"
              onClick={() => navigate(destination)}
            >
              <span>{label}</span>
              <span className="submit-arrow">→</span>
            </button>
          </div>
        </div>
      </section>
    </main>
  );
}

export default NotFound;
