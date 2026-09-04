import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import { verifyEmail } from "../services/authService";
import Brand from "../components/Brand";
import "../styles/auth.css";

function VerifyEmail() {
  const location = useLocation();
  const navigate = useNavigate();
  const verificationStarted = useRef(false);

  const [status, setStatus] = useState("verifying");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (verificationStarted.current) return;
  
    verificationStarted.current = true;
  
    const token = new URLSearchParams(location.search).get("token");
  
    if (!token) {
      setStatus("error");
      setMessage("Invalid verification link.");
      return;
    }
  
    const verify = async () => {
      try {
        const result = await verifyEmail(token);
  
        setStatus("success");
        setMessage(
          result.message ||
            "Email verified successfully. You can now sign in."
        );
      } catch (error) {
        setStatus("error");
        setMessage(error.message || "Unable to verify your email.");
      }
    };
  
    verify();
  }, [location.search]);

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

              {status === "verifying" && (
                <>
                  <h2>Verifying your email</h2>
                  <p>Please wait while we verify your email address.</p>
                </>
              )}

              {status === "success" && (
                <>
                  <h2>Email verified ✓</h2>
                  <p>{message}</p>

                  <button
                    type="button"
                    className="auth-submit"
                    onClick={() => navigate("/login")}
                  >
                    <span>Continue to sign in</span>
                    <span className="submit-arrow">→</span>
                  </button>
                </>
              )}

              {status === "error" && (
                <>
                  <h2>Verification failed</h2>
                  <p>{message}</p>

                  <button
                    type="button"
                    className="auth-submit"
                    onClick={() => navigate("/login")}
                  >
                    <span>Go to sign in</span>
                    <span className="submit-arrow">→</span>
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

export default VerifyEmail;