import { useEffect, useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import { SETTINGS_NAV } from "../components/layout/nav-items";
import { getCurrentUser } from "../api/auth";
import "../styles/workspace.css";

function Settings() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadUser = async () => {
      try {
        const currentUser = await getCurrentUser();
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
    <AppLayout
      status="SETTINGS"
      sidebarProps={{ items: SETTINGS_NAV, placement: "bottom" }}
    >
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
                <span>
                  {loading
                    ? "Loading account..."
                    : error
                      ? error
                      : user
                        ? `${user.username} · ${user.email}`
                        : "Profile and account preferences"}
                </span>
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
    </AppLayout>
  );
}

export default Settings;