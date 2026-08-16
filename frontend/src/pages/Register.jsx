import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Brand from "../components/Brand";
import "../styles/auth.css";

function Register() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (form.password !== form.confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    console.log("Registration:", form);
  };

  return (
    <main className="auth-page">
      <section className="auth-shell register-shell">
        {/* Left side */}
        <div className="auth-visual">
          <div className="auth-glow auth-glow-one" />
          <div className="auth-glow auth-glow-two" />

          <div className="auth-visual-content">
            <Brand />

            <div className="auth-hero register-hero">
              <div className="eyebrow">
                <span className="status-dot" />
                YOUR WORKSPACE STARTS HERE
              </div>

              <h1>
                Build your
                <br />
                <span>intelligent workspace.</span>
              </h1>

              <p>
                Bring your knowledge, tools, and workflows together
                in one place with WorkMind.
              </p>
            </div>

            <div className="workspace-preview">
              <div className="preview-header">
                <span className="preview-dot" />
                WORKMIND WORKSPACE
                <span className="preview-status">READY</span>
              </div>

              <div className="preview-content">
                <div className="preview-sidebar">
                  <span />
                  <span />
                  <span />
                  <span />
                </div>

                <div className="preview-main">
                  <div className="preview-line preview-line-large" />
                  <div className="preview-line" />
                  <div className="preview-line preview-line-short" />

                  <div className="preview-cards">
                    <div />
                    <div />
                    <div />
                  </div>
                </div>
              </div>
            </div>

            <div className="auth-quote">
              <span>“</span>
              <p>Turn information into action.</p>
            </div>
          </div>
        </div>

        {/* Right side */}
        <div className="auth-form-panel">
          <div className="auth-form-container">
            <div className="mobile-brand">
              <Brand compact />
            </div>

            <div className="form-heading">
              <span className="form-kicker">GET STARTED</span>
              <h2>Create your workspace</h2>
              <p>Set up your WorkMind account in a few seconds.</p>
            </div>

            <form onSubmit={handleSubmit} className="auth-form">
              <div className="field">
                <label htmlFor="name">Full name</label>

                <div className="input-wrap">
                  <span className="input-icon">✦</span>

                  <input
                    id="name"
                    name="name"
                    type="text"
                    placeholder="Your name"
                    value={form.name}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              <div className="field">
                <label htmlFor="register-email">Email</label>

                <div className="input-wrap">
                  <span className="input-icon">@</span>

                  <input
                    id="register-email"
                    name="email"
                    type="email"
                    placeholder="you@example.com"
                    value={form.email}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              <div className="field">
                <label htmlFor="register-password">Password</label>

                <div className="input-wrap">
                  <span className="input-icon">●</span>

                  <input
                    id="register-password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Create a password"
                    value={form.password}
                    onChange={handleChange}
                    minLength={8}
                    required
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() => setShowPassword((value) => !value)}
                  >
                    {showPassword ? "Hide" : "Show"}
                  </button>
                </div>

                <small className="field-hint">
                  Use at least 8 characters.
                </small>
              </div>

              <div className="field">
                <label htmlFor="confirm-password">
                  Confirm password
                </label>

                <div className="input-wrap">
                  <span className="input-icon">●</span>

                  <input
                    id="confirm-password"
                    name="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder="Repeat your password"
                    value={form.confirmPassword}
                    onChange={handleChange}
                    minLength={8}
                    required
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowConfirmPassword((value) => !value)
                    }
                  >
                    {showConfirmPassword ? "Hide" : "Show"}
                  </button>
                </div>
              </div>

              <button type="submit" className="auth-submit">
                <span>Create workspace</span>
                <span className="submit-arrow">→</span>
              </button>
            </form>

            <p className="auth-footer register-footer">
              Already have an account?
              <button
                type="button"
                onClick={() => navigate("/login")}
              >
                Sign in
              </button>
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}

export default Register;