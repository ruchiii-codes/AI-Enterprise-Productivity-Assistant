import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import Brand from "../components/Brand";
import { resetPassword } from "../api/auth";
import "../styles/auth.css";

const MIN_PASSWORD_LENGTH = 8;

function ResetPassword() {
  const location = useLocation();
  const navigate = useNavigate();

  // Read once at render, the same way VerifyEmail does.
  const token = new URLSearchParams(location.search).get("token");

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    if (password.length < MIN_PASSWORD_LENGTH) {
      setError(`Use at least ${MIN_PASSWORD_LENGTH} characters.`);
      return;
    }

    setLoading(true);

    try {
      await resetPassword(token, password);

      setDone(true);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  };

  // A link with no token cannot be acted on at all.
  if (!token) {
    return (
      <main className="auth-page">
        <section className="auth-shell">
          <div className="auth-form-panel">
            <div className="auth-form-container">
              <div className="mobile-brand">
                <Brand compact />
              </div>

              <div className="form-heading">
                <span className="form-kicker">WORKMIND</span>

                <h2>Invalid reset link</h2>

                <p>
                  This password reset link is missing its token. Request a
                  new one and try again.
                </p>
              </div>

              <button
                type="button"
                className="auth-submit"
                onClick={() => navigate("/forgot-password")}
              >
                <span>Request a new link</span>
                <span className="submit-arrow">→</span>
              </button>
            </div>
          </div>
        </section>
      </main>
    );
  }

  if (done) {
    return (
      <main className="auth-page">
        <section className="auth-shell">
          <div className="auth-form-panel">
            <div className="auth-form-container">
              <div className="mobile-brand">
                <Brand compact />
              </div>

              <div className="form-heading">
                <span className="form-kicker">WORKMIND</span>

                <h2>Password updated</h2>

                <p>
                  Your password has been reset. You can now sign in with your
                  new password.
                </p>
              </div>

              <button
                type="button"
                className="auth-submit"
                onClick={() => navigate("/login")}
              >
                <span>Continue to sign in</span>
                <span className="submit-arrow">→</span>
              </button>
            </div>
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className="auth-page">
      <section className="auth-shell">
        <div className="auth-form-panel">
          <div className="auth-form-container">
            <div className="mobile-brand">
              <Brand compact />
            </div>

            <div className="form-heading">
              <span className="form-kicker">RESET PASSWORD</span>

              <h2>Choose a new password</h2>

              <p>Pick something you have not used before.</p>
            </div>

            <form onSubmit={handleSubmit} className="auth-form">
              <div className="field">
                <label htmlFor="password">New password</label>

                <div className="input-wrap">
                  <span className="input-icon">●</span>

                  <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter a new password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    minLength={MIN_PASSWORD_LENGTH}
                    required
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() => setShowPassword((value) => !value)}
                    aria-label={
                      showPassword ? "Hide password" : "Show password"
                    }
                  >
                    {showPassword ? "Hide" : "Show"}
                  </button>
                </div>

                <small className="field-hint">
                  Use at least {MIN_PASSWORD_LENGTH} characters.
                </small>
              </div>

              <div className="field">
                <label htmlFor="confirmPassword">Confirm new password</label>

                <div className="input-wrap">
                  <span className="input-icon">●</span>

                  <input
                    id="confirmPassword"
                    type={showPassword ? "text" : "password"}
                    placeholder="Re-enter your new password"
                    value={confirmPassword}
                    onChange={(event) =>
                      setConfirmPassword(event.target.value)
                    }
                    minLength={MIN_PASSWORD_LENGTH}
                    required
                  />
                </div>
              </div>

              {error && <div className="auth-error">{error}</div>}

              <button
                type="submit"
                className="auth-submit"
                disabled={loading}
              >
                <span>{loading ? "Updating..." : "Update password"}</span>
                <span className="submit-arrow">{loading ? "..." : "→"}</span>
              </button>
            </form>
          </div>
        </div>
      </section>
    </main>
  );
}

export default ResetPassword;
