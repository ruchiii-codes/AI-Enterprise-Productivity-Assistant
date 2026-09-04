import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Brand from "../components/Brand";
import "../styles/workspace.css";
import ProfileMenu from "../components/ProfileMenu";

function Tools() {
  const [error, setError] = useState("");
  // GitHub state
  const [githubConnected, setGithubConnected] = useState(false);
  const [githubUsername, setGithubUsername] = useState(null);
  const [githubLoading, setGithubLoading] = useState(true);

  // Gmail state
  const [gmailConnected, setGmailConnected] = useState(false);
  const [gmailEmail, setGmailEmail] = useState(null);
  const [gmailLoading, setGmailLoading] = useState(true);

  // Calendar state
  const [calendarConnected, setCalendarConnected] = useState(false);
  const [calendarEmail, setCalendarEmail] = useState(null);
  const [calendarLoading, setCalendarLoading] = useState(true);

  useEffect(() => {
    async function checkConnections() {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setGithubLoading(false);
        setGmailLoading(false);
        setCalendarLoading(false);
        return;
      }

      // -------------------------
      // GitHub status
      // -------------------------
      try {
        const response = await fetch(
          "http://localhost:8000/auth/github/status",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to check GitHub connection.");
        }

        const data = await response.json();

        setGithubConnected(data.connected);
        setGithubUsername(data.username);
      } catch (error) {
        console.error("GitHub status error:", error);
        setError("Unable to check GitHub connection.");
        setGithubConnected(false);
        setGithubUsername(null);
      } finally {
        setGithubLoading(false);
      }

      // -------------------------
      // Gmail status
      // -------------------------
      try {
        const response = await fetch(
          "http://localhost:8000/auth/gmail/status",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to check Gmail connection.");
        }

        const data = await response.json();

        setGmailConnected(data.connected);
        setGmailEmail(data.email);
      } catch (error) {
        console.error("Gmail status error:", error);
        setError("Unable to check Gmail connection.");
        setGmailConnected(false);
        setGmailEmail(null);
      } finally {
        setGmailLoading(false);
      }

      // -------------------------
      // Calendar status
      // -------------------------
      try {
        const response = await fetch(
          "http://localhost:8000/auth/calendar/status",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to check Calendar connection.");
        }

        const data = await response.json();

        setCalendarConnected(data.connected);
        setCalendarEmail(data.email);
      } catch (error) {
        console.error("Calendar status error:", error);
        setError("Unable to check Calendar connection.");
        setCalendarConnected(false);
        setCalendarEmail(null);
      } finally {
        setCalendarLoading(false);
      }
    }

    checkConnections();
  }, []);

  // -------------------------
  // GitHub connect
  // -------------------------
  const connectGitHub = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("Please log in again.");
      return;
    }

    try {
      const response = await fetch(
        "http://localhost:8000/auth/github/start",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to start GitHub connection.");
      }

      const data = await response.json();

      window.location.href = data.authorization_url;
    } catch (error) {
      console.error("GitHub connection error:", error);
      setError("Unable to connect GitHub. Please try again.");
    }
  };

  // -------------------------
  // GitHub disconnect
  // -------------------------
  const disconnectGitHub = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      return;
    }

    try {
      const response = await fetch(
        "http://localhost:8000/auth/github/disconnect",
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to disconnect GitHub.");
      }

      setGithubConnected(false);
      setGithubUsername(null);
    } catch (error) {
      console.error("GitHub disconnect error:", error);
      setError("Unable to disconnect GitHub. Please try again.");
    }
  };

  // -------------------------
  // Gmail connect
  // -------------------------
  const connectGmail = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Please log in again.");
      return;
    }

    try {
      const response = await fetch(
        "http://localhost:8000/auth/gmail/start",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to start Gmail connection.");
      }

      const data = await response.json();

      window.location.href = data.authorization_url;
    } catch (error) {
      console.error("Gmail connection error:", error);
      alert("Unable to connect Gmail. Please try again.");
    }
  };

  // -------------------------
  // Gmail disconnect
  // -------------------------
  const disconnectGmail = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      return;
    }

    try {
      const response = await fetch(
        "http://localhost:8000/auth/gmail/disconnect",
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to disconnect Gmail.");
      }

      setGmailConnected(false);
      setGmailEmail(null);
    } catch (error) {
      console.error("Gmail disconnect error:", error);
      alert("Unable to disconnect Gmail. Please try again.");
    }
  };

  // -------------------------
  // Calendar connect
  // -------------------------
  const connectCalendar = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Please log in again.");
      return;
    }

    try {
      const response = await fetch(
        "http://localhost:8000/auth/calendar/start",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to start Calendar connection.");
      }

      const data = await response.json();

      window.location.href = data.authorization_url;
    } catch (error) {
      console.error("Calendar connection error:", error);
      alert("Unable to connect Calendar. Please try again.");
    }
  };

  // -------------------------
  // Calendar disconnect
  // -------------------------
  const disconnectCalendar = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      return;
    }

    try {
      const response = await fetch(
        "http://localhost:8000/auth/calendar/disconnect",
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to disconnect Calendar.");
      }

      setCalendarConnected(false);
      setCalendarEmail(null);
    } catch (error) {
      console.error("Calendar disconnect error:", error);
      alert("Unable to disconnect Calendar. Please try again.");
    }
  };

  return (
    <main className="workspace-page">
      {error && (
        <div className="tools-error">
          <span>!</span>
          <span>{error}</span>
      
          <button
            type="button"
            onClick={() => setError("")}
            aria-label="Dismiss error"
          >
            ×
          </button>
        </div>
      )}
      <aside className="workspace-sidebar">
        <div className="sidebar-top">
          <Brand compact />

          <Link to="/workspace" className="new-chat-button">
            <span>←</span>
            <span>Back to workspace</span>
          </Link>

          <div className="sidebar-section">
            <div className="sidebar-label">WORKSPACE</div>

            <Link to="/workspace" className="workspace-nav">
              <span>⌂</span>
              Overview
            </Link>

            <Link to="/knowledge" className="workspace-nav">
              <span>✦</span>
              Knowledge
            </Link>

            <Link to="/agents" className="workspace-nav">
              <span>◇</span>
              Agents
            </Link>

            <Link to="/tools" className="workspace-nav active">
              <span>⌁</span>
              Connected tools
            </Link>
          </div>
        </div>
      </aside>

      <section className="workspace-main">
        <header className="workspace-header">
          <span className="header-status">
            <span />
            TOOL CONNECTIONS
          </span>

          <div className="header-actions">
            <ProfileMenu />
          </div>
        </header>

        <div className="workspace-content">
          <section className="workspace-hero">
            <div>
              <span className="hero-kicker">CONNECTED TOOLS</span>

              <h1>
                Your tools.
                <br />
                <span>One intelligence layer.</span>
              </h1>

              <p>
                Connect the services you use every day and
                let WorkMind work across them.
              </p>
            </div>
          </section>

          <section className="capability-grid">

            {/* Gmail */}
            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">G</div>
                <span>●</span>
              </div>

              <div className="card-content">
                <span className="card-label">EMAIL</span>

                <h3>Gmail</h3>

                <p>
                  Search and work with your email through
                  WorkMind.
                </p>
              </div>

              <div className="agent-status">
                {gmailLoading ? (
                  <>
                    <span className="pulse-dot" />
                    Checking connection...
                  </>
                ) : gmailConnected ? (
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      gap: "6px",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                      }}
                    >
                      <span className="pulse-dot" />
                      <span>Connected</span>
                    </div>

                    {gmailEmail && (
                      <span
                        style={{
                          fontSize: "16px",
                          fontWeight: "600",
                          marginLeft: "16px",
                        }}
                      >
                        {gmailEmail}
                      </span>
                    )}

                    <button
                      type="button"
                      onClick={disconnectGmail}
                      style={{
                        marginTop: "8px",
                        width: "fit-content",
                        cursor: "pointer",
                      }}
                    >
                      Disconnect
                    </button>
                  </div>
                ) : (
                  <>
                    <span className="pulse-dot" />

                    <button
                      type="button"
                      onClick={connectGmail}
                    >
                      Connect Gmail
                    </button>
                  </>
                )}
              </div>
            </div>

            {/* Calendar */}
            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">C</div>
                <span>●</span>
              </div>

              <div className="card-content">
                <span className="card-label">SCHEDULE</span>

                <h3>Calendar</h3>

                <p>
                  Access and manage your schedule through
                  WorkMind.
                </p>
              </div>

              <div className="agent-status">
                {calendarLoading ? (
                  <>
                    <span className="pulse-dot" />
                    Checking connection...
                  </>
                ) : calendarConnected ? (
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      gap: "6px",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                      }}
                    >
                      <span className="pulse-dot" />
                      <span>Connected</span>
                    </div>

                    {calendarEmail && (
                      <span
                        style={{
                          fontSize: "16px",
                          fontWeight: "600",
                          marginLeft: "16px",
                        }}
                      >
                        {calendarEmail}
                      </span>
                    )}

                    <button
                      type="button"
                      onClick={disconnectCalendar}
                      style={{
                        marginTop: "8px",
                        width: "fit-content",
                        cursor: "pointer",
                      }}
                    >
                      Disconnect
                    </button>
                  </div>
                ) : (
                  <>
                    <span className="pulse-dot" />

                    <button
                      type="button"
                      onClick={connectCalendar}
                    >
                      Connect Calendar
                    </button>
                  </>
                )}
              </div>
            </div>

            {/* GitHub */}
            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">GH</div>

                <span>●</span>
              </div>

              <div className="card-content">
                <span className="card-label">DEVELOPMENT</span>

                <h3>GitHub</h3>

                <p>
                  Search repositories, issues, and development
                  activity.
                </p>
              </div>

              <div className="agent-status">
                {githubLoading ? (
                  <>
                    <span className="pulse-dot" />
                    Checking connection...
                  </>
                ) : githubConnected ? (
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      gap: "6px",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                      }}
                    >
                      <span className="pulse-dot" />
                      <span>Connected</span>
                    </div>

                    {githubUsername && (
                      <span
                        style={{
                          fontSize: "16px",
                          fontWeight: "600",
                          marginLeft: "16px",
                        }}
                      >
                        {githubUsername}
                      </span>
                    )}

                    <button
                      type="button"
                      onClick={disconnectGitHub}
                      style={{
                        marginTop: "8px",
                        width: "fit-content",
                        cursor: "pointer",
                      }}
                    >
                      Disconnect
                    </button>
                  </div>
                ) : (
                  <>
                    <span className="pulse-dot" />

                    <button
                      type="button"
                      onClick={connectGitHub}
                    >
                      Connect GitHub
                    </button>
                  </>
                )}
              </div>
            </div>

          </section>
        </div>
      </section>
    </main>
  );
}

export default Tools;