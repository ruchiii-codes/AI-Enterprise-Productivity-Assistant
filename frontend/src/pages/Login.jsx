import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Brand from "../components/ui/Brand";
import Field from "../components/ui/Field";
import PasswordField from "../components/ui/PasswordField";
import { useAuth } from "../hooks/useAuth";
import "../styles/auth.css";

function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Where ProtectedRoute wanted to send them before the redirect to login.
  const destination = location.state?.from?.pathname || "/workspace";

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await login(email, password);

      navigate(destination, { replace: true });
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-shell">
        {/* Left: WorkMind identity */}
        <div className="auth-visual">
          <div className="auth-glow auth-glow-one" />
          <div className="auth-glow auth-glow-two" />

          <div className="auth-visual-content">
            <Brand />

            <div className="auth-hero">
              <div className="eyebrow">
                <span className="status-dot" />
                INTELLIGENT WORKSPACE
              </div>

              <h1>
                Your work,
                <br />
                <span>with a mind.</span>
              </h1>

              <p>
                One intelligent workspace for your knowledge,
                productivity, and everyday work.
              </p>
            </div>

            <div className="capability-list">
              <div className="capability">
                <span>✦</span>
                <div>
                  <strong>Knowledge</strong>
                  <small>Search and understand your documents</small>
                </div>
              </div>

              <div className="capability">
                <span>◈</span>
                <div>
                  <strong>AI Agents</strong>
                  <small>Plan and execute complex tasks</small>
                </div>
              </div>

              <div className="capability">
                <span>⌁</span>
                <div>
                  <strong>Productivity</strong>
                  <small>Connect the tools you already use</small>
                </div>
              </div>
            </div>

            <div className="auth-quote">
              <span>“</span>
              <p>One workspace. Every capability.</p>
            </div>
          </div>
        </div>

        {/* Right: Login form */}
        <div className="auth-form-panel">
          <div className="auth-form-container">
            <div className="mobile-brand">
              <Brand compact />
            </div>

            <div className="form-heading">
              <span className="form-kicker">WELCOME BACK</span>
              <h2>Sign in to WorkMind</h2>
              <p>Continue where you left off.</p>
            </div>

            <form onSubmit={handleSubmit} className="auth-form">
              <Field
                id="email"
                label="Email"
                icon="@"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />

              <PasswordField
                id="password"
                label="Password"
                icon="●"
                placeholder="Enter your password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
                visible={showPassword}
                onToggleVisibility={() => setShowPassword((value) => !value)}
                labelAction={
                  <button
                    type="button"
                    className="forgot-button"
                    onClick={() => navigate("/forgot-password")}
                  >
                    Forgot password?
                  </button>
                }
              />
              
              {error && (
                <div className="auth-error">
                  {error}
                </div>
              )}

              <button
                type="submit"              
                className="auth-submit"
                disabled={loading}
              >
                <span>              
                  {loading ? "Signing in..." : "Sign in"}
                </span>

                <span className="submit-arrow">
                  {loading ? "..." : "→"}
                </span>
              </button>
            </form>

            <p className="auth-footer">
              Don't have an account?
              <button type="button" onClick={() => navigate("/register")}>
                Create one
              </button>
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}

export default Login;