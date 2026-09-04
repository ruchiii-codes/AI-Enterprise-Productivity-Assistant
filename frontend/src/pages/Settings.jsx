import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Brand from "../components/Brand";
import { getCurrentUser } from "../services/authService";
import "../styles/workspace.css";

function Settings() {
  function Settings() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setError("Authentication token not found.");
        setLoading(false);
        return;
      }

      try {
        const currentUser = await getCurrentUser(token);
        setUser(currentUser);
      } catch (err) {
        setError(err.message || "Unable to load account information.");
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  return (
    <main className="workspace-page">
      <aside className="workspace-sidebar">
        <div className="sidebar-top">
          <Brand compact />

          <Link to="/workspace" className="new-chat-button">
            <span>←</span>
            <span>Back to workspace</span>
          </Link>
        </div>

        <div className="sidebar-bottom">
          <Link to="/workspace" className="workspace-nav">
            <span>⌂</span>
            Workspace
          </Link>

          <Link to="/settings" className="workspace-nav active">
            <span>⚙</span>
            Settings
          </Link>
        </div>
      </aside>

      <section className="workspace-main">
        <header className="workspace-header">
          <span className="header-status">
            <span />
            SETTINGS
          </span>
        </header>

        <div className="workspace-content">
          <section className="workspace-hero">
            <div>
              <span className="hero-kicker">WORKSPACE SETTINGS</span>

              <h1>
                Make WorkMind
                <br />
                <span>work your way.</span>
              </h1>

              <p>
                Manage your workspace preferences,
                integrations, and account settings.
              </p>
            </div>
          </section>

          <section className="activity-list">
            <div className="activity-item">
              <div className="activity-icon">◉</div>
              <div>
                <strong>Account</strong>
                <span>Profile and account preferences</span>
              </div>
              <span>→</span>
            </div>

            <div className="activity-item">
              <div className="activity-icon">✦</div>
              <div>
                <strong>AI preferences</strong>
                <span>Configure how WorkMind responds</span>
              </div>
              <span>→</span>
            </div>

            <div className="activity-item">
              <div className="activity-icon">⌁</div>
              <div>
                <strong>Integrations</strong>
                <span>Manage connected services</span>
              </div>
              <span>→</span>
            </div>

            <div className="activity-item">
              <div className="activity-icon">◇</div>
              <div>
                <strong>Security</strong>
                <span>Authentication and session settings</span>
              </div>
              <span>→</span>
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}
}

export default Settings;