import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Brand from "../components/Brand";
import { requestPasswordReset } from "../api/auth";
import "../styles/auth.css";

function ForgotPassword() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [submittedEmail, setSubmittedEmail] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await requestPasswordReset(email);

      // The backend answers identically for unknown addresses, so this
      // confirmation deliberately does not claim the account exists.
      setSubmittedEmail(email);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  };

  if (submittedEmail) {
    return (
      <main className="auth-page">
        <section className="auth-shell">
          <div className="auth-form-panel">
            <div className="auth-form-container">
              <div className="mobile-brand">
                <Brand compact />
              </div>

              <div className="form-heading">
                <span className="form-kicker">CHECK YOUR EMAIL</span>

                <h2>Reset link sent</h2>

                <p>
                  If <strong>{submittedEmail}</strong> has a WorkMind
                  account, a password reset link is on its way. The link
                  expires in 1 hour and can only be used once.
                </p>
              </div>

              <button
                type="button"
                className="auth-submit"
                onClick={() => navigate("/login")}
              >
                <span>Back to sign in</span>
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
              <span className="form-kicker">FORGOT PASSWORD</span>

              <h2>Reset your password</h2>

              <p>
                Enter the email address on your account and we will send you
                a link to choose a new password.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="auth-form">
              <div className="field">
                <label htmlFor="email">Email</label>

                <div className="input-wrap">
                  <span className="input-icon">@</span>

                  <input
                    id="email"
                    type="email"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
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
                <span>{loading ? "Sending..." : "Send reset link"}</span>
                <span className="submit-arrow">{loading ? "..." : "→"}</span>
              </button>
            </form>

            <p className="auth-footer">
              Remembered it?
              <button type="button" onClick={() => navigate("/login")}>
                Sign in
              </button>
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}

export default ForgotPassword;
