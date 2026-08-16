import { Link } from "react-router-dom";
import Brand from "../components/Brand";
import "../styles/workspace.css";

function Tools() {
  return (
    <main className="workspace-page">
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

        <div className="sidebar-bottom">
          <Link to="/settings" className="workspace-nav">
            <span>⚙</span>
            Settings
          </Link>
        </div>
      </aside>

      <section className="workspace-main">
        <header className="workspace-header">
          <span className="header-status">
            <span />
            TOOL CONNECTIONS
          </span>
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
                <span className="pulse-dot" />
                Ready to connect
              </div>
            </div>

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
                <span className="pulse-dot" />
                Ready to connect
              </div>
            </div>

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
                <span className="pulse-dot" />
                Ready to connect
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

export default Tools;