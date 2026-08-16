import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Brand from "../components/Brand";
import { loginUser } from "../services/authService";
import "../styles/auth.css";

function Login() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const data = await loginUser(email, password);

      localStorage.setItem("access_token", data.access_token);

      navigate("/workspace");
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

              <div className="field">
                <div className="field-label-row">
                  <label htmlFor="password">Password</label>
                  <button
                    type="button"
                    className="forgot-button"
                    onClick={() => console.log("Forgot password")}
                  >
                    Forgot password?
                  </button>
                </div>

                <div className="input-wrap">
                  <span className="input-icon">●</span>

                  <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter your password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
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
              </div>
              
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

            <div className="auth-divider">
              <span>OR</span>
            </div>

            <button
              type="button"
              className="demo-button"
              onClick={() => console.log("Demo mode")}
            >
              <span>Explore demo workspace</span>
              <span>↗</span>
            </button>

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