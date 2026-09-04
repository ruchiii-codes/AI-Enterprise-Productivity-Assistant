import { Link } from "react-router-dom";
import Brand from "../components/Brand";
import "../styles/workspace.css";
import ProfileMenu from "../components/ProfileMenu";

function Agents() {
  return (
    <main className="workspace-page">
      {/* Sidebar */}
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

            <Link to="/agents" className="workspace-nav active">
              <span>◇</span>
              Agents
            </Link>

            <Link to="/tools" className="workspace-nav">
              <span>⌁</span>
              Connected tools
            </Link>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <section className="workspace-main">
        {/* Header */}
        <header className="workspace-header">
          <span className="header-status">
            <span />
            AGENTS ONLINE
          </span>

          <div className="header-actions">
            <ProfileMenu />
          </div>
        </header>

        <div className="workspace-content">
          {/* Hero */}
          <section className="workspace-hero">
            <div>
              <span className="hero-kicker">AI AGENTS</span>

              <h1>
                Your AI teammates,
                <br />
                <span>ready to help.</span>
              </h1>

              <p>
                WorkMind can handle different kinds of work
                so you can focus on what matters.
              </p>
            </div>
          </section>

          {/* Agents */}
          <section>
            <div className="knowledge-section-header">
              <span className="card-label">YOUR AI AGENTS</span>
            </div>

            <div className="capability-grid">
              {/* Research & Knowledge */}
              <div className="dashboard-card">
                <div className="card-top">
                  <div className="dashboard-icon">✦</div>
                </div>

                <div className="card-content">
                  <span className="card-label">
                    RESEARCH & KNOWLEDGE
                  </span>

                  <h3>Research & Knowledge</h3>

                  <p>
                    Find relevant information from your
                    connected knowledge and get useful answers.
                  </p>
                </div>

                <div className="agent-status">
                  <span className="pulse-dot" />
                  Ready
                </div>
              </div>

              {/* Planning */}
              <div className="dashboard-card">
                <div className="card-top">
                  <div className="dashboard-icon">◇</div>
                </div>

                <div className="card-content">
                  <span className="card-label">
                    PLANNING
                  </span>

                  <h3>Planning</h3>

                  <p>
                    Break complex work into clear,
                    actionable steps.
                  </p>
                </div>

                <div className="agent-status">
                  <span className="pulse-dot" />
                  Ready
                </div>
              </div>

              {/* Summarization */}
              <div className="dashboard-card">
                <div className="card-top">
                  <div className="dashboard-icon">≡</div>
                </div>

                <div className="card-content">
                  <span className="card-label">
                    SUMMARIZATION
                  </span>

                  <h3>Summarization</h3>

                  <p>
                    Turn large amounts of information
                    into concise, useful results.
                  </p>
                </div>

                <div className="agent-status">
                  <span className="pulse-dot" />
                  Ready
                </div>
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

export default Agents;