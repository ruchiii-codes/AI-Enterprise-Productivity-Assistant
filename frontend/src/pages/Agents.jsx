import { Link } from "react-router-dom";
import Brand from "../components/Brand";
import "../styles/workspace.css";

function Agents() {
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
            AGENT SYSTEM
          </span>
        </header>

        <div className="workspace-content">
          <section className="workspace-hero">
            <div>
              <span className="hero-kicker">AI AGENTS</span>

              <h1>
                Don't just ask AI.
                <br />
                <span>Let it work.</span>
              </h1>

              <p>
                WorkMind agents can plan, retrieve information,
                use tools, and complete multi-step tasks.
              </p>
            </div>

            <div className="hero-orbit">
              <div className="orbit-ring orbit-ring-one" />
              <div className="orbit-ring orbit-ring-two" />
              <div className="orbit-core">◇</div>
              <span className="orbit-dot orbit-dot-one" />
              <span className="orbit-dot orbit-dot-two" />
              <span className="orbit-dot orbit-dot-three" />
            </div>
          </section>

          <section className="capability-grid">
            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">◇</div>
              </div>

              <div className="card-content">
                <span className="card-label">PLANNER</span>
                <h3>Planner Agent</h3>
                <p>
                  Break complex requests into smaller,
                  actionable steps.
                </p>
              </div>

              <div className="agent-status">
                <span className="pulse-dot" />
                Available
              </div>
            </div>

            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">✦</div>
              </div>

              <div className="card-content">
                <span className="card-label">RETRIEVER</span>
                <h3>Retriever Agent</h3>
                <p>
                  Find and select the most relevant knowledge
                  for each task.
                </p>
              </div>

              <div className="agent-status">
                <span className="pulse-dot" />
                Available
              </div>
            </div>

            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">≡</div>
              </div>

              <div className="card-content">
                <span className="card-label">SUMMARY</span>
                <h3>Summary Agent</h3>
                <p>
                  Turn large amounts of information into
                  concise, useful results.
                </p>
              </div>

              <div className="agent-status">
                <span className="pulse-dot" />
                Available
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

export default Agents;