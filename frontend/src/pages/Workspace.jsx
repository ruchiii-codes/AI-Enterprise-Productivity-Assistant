import { Link } from "react-router-dom";
import Brand from "../components/Brand";
import "../styles/workspace.css";

function Workspace() {
  return (
    <main className="workspace-page">
      {/* Sidebar */}
      <aside className="workspace-sidebar">
        <div className="sidebar-top">
          <Brand compact />

          <button className="new-chat-button">
            <span>+</span>
            <span>New conversation</span>
            <kbd>⌘ K</kbd>
          </button>

          <div className="sidebar-section">
            <div className="sidebar-label">
              CONVERSATIONS
            </div>

            <button className="conversation active">
              <span className="conversation-icon">✦</span>
              <span>Project research</span>
            </button>

            <button className="conversation">
              <span className="conversation-icon">◌</span>
              <span>RAG architecture</span>
            </button>

            <button className="conversation">
              <span className="conversation-icon">◌</span>
              <span>Weekly planning</span>
            </button>
          </div>

          <div className="sidebar-section">
            <div className="sidebar-label">
              WORKSPACE
            </div>

            <button className="workspace-nav active">
              <span>⌂</span>
              Overview
            </button>

            <button className="workspace-nav">
              <span>✦</span>
              Knowledge
            </button>

            <button className="workspace-nav">
              <span>◇</span>
              Agents
            </button>

            <button className="workspace-nav">
              <span>⌁</span>
              Connected tools
            </button>
          </div>
        </div>

        <div className="sidebar-bottom">
          <button className="workspace-nav">
            <span>⚙</span>
            Settings
          </button>

          <div className="user-mini">
            <div className="user-avatar">R</div>

            <div>
              <strong>Ruchika</strong>
              <small>Personal workspace</small>
            </div>

            <span className="user-more">•••</span>
          </div>
        </div>
      </aside>

      {/* Main workspace */}
      <section className="workspace-main">
        <header className="workspace-header">
          <div>
            <span className="header-status">
              <span />
              WORKMIND ONLINE
            </span>
          </div>

          <div className="header-actions">
            <button className="header-button">
              ⌕ <span>Search</span>
              <kbd>⌘ K</kbd>
            </button>

            <button className="icon-button">
              ♢
            </button>

            <button className="icon-button">
              ?
            </button>

            <div className="header-avatar">R</div>
          </div>
        </header>

        <div className="workspace-content">
          {/* Hero */}
          <section className="workspace-hero">
            <div>
              <span className="hero-kicker">
                YOUR INTELLIGENT WORKSPACE
              </span>

              <h1>
                Good morning, Ruchika.
                <br />
                <span>What are we working on?</span>
              </h1>

              <p>
                Ask WorkMind anything, search your knowledge,
                or let an agent take care of a task.
              </p>
            </div>

            <div className="hero-orbit">
              <div className="orbit-ring orbit-ring-one" />
              <div className="orbit-ring orbit-ring-two" />
              <div className="orbit-core">✦</div>

              <span className="orbit-dot orbit-dot-one" />
              <span className="orbit-dot orbit-dot-two" />
              <span className="orbit-dot orbit-dot-three" />
            </div>
          </section>

          {/* Capability cards */}
          <section className="capability-grid">
            <Link to="/knowledge" className="dashboard-card knowledge-card">
              <div className="card-top">
                <div className="dashboard-icon">✦</div>
                <span>→</span>
              </div>

              <div className="card-content">
                <span className="card-label">KNOWLEDGE</span>
                <h3>Your knowledge, connected.</h3>
                <p>
                  Search documents and get answers with
                  grounded sources.
                </p>
              </div>

              <div className="card-metric">
                <strong>24</strong>
                <span>documents indexed</span>
              </div>
            </Link>

            <Link to="/agents" className="dashboard-card agents-card">
              <div className="card-top">
                <div className="dashboard-icon">◇</div>
                <span>→</span>
              </div>

              <div className="card-content">
                <span className="card-label">AGENTS</span>
                <h3>Let AI do the work.</h3>
                <p>
                  Plan complex tasks and execute them
                  across connected tools.
                </p>
              </div>

              <div className="agent-status">
                <span className="pulse-dot" />
                3 agents available
              </div>
            </Link>

            <Link to="/tools" className="dashboard-card tools-card">
              <div className="card-top">
                <div className="dashboard-icon">⌁</div>
                <span>→</span>
              </div>

              <div className="card-content">
                <span className="card-label">TOOLS</span>
                <h3>Everything in one place.</h3>
                <p>
                  Connect the services you already use
                  every day.
                </p>
              </div>

              <div className="tool-icons">
                <span>G</span>
                <span>C</span>
                <span>GH</span>
              </div>
            </Link>
          </section>

          {/* AI command center */}
          <section className="command-section">
            <div className="section-heading">
              <div>
                <span className="section-kicker">
                  COMMAND CENTER
                </span>

                <h2>Ask WorkMind</h2>
              </div>

              <span className="model-status">
                <span />
                AI READY
              </span>
            </div>

            <Link to="/chat" className="command-box">
              <div className="command-icon">
                ✦
              </div>

              <div className="command-placeholder">
                <span>
                  Ask anything about your work...
                </span>

                <small>
                  Search knowledge · analyze information ·
                  execute tasks
                </small>
              </div>

              <button className="command-attach">
                +
              </button>

              <button className="command-send">
                ↑
              </button>
            </Link>
            <div className="suggestions">
              <button>
                Summarize my recent project updates
              </button>

              <button>
                Find documents about RAG
              </button>

              <button>
                What should I work on today?
              </button>
            </div>
          </section>

          {/* Activity */}
          <section className="activity-section">
            <div className="section-heading">
              <div>
                <span className="section-kicker">
                  ACTIVITY
                </span>

                <h2>Recent work</h2>
              </div>

              <button className="view-all">
                View all →
              </button>
            </div>

            <div className="activity-list">
              <div className="activity-item">
                <div className="activity-icon">✦</div>

                <div>
                  <strong>
                    Knowledge base updated
                  </strong>

                  <span>
                    3 documents were successfully indexed
                  </span>
                </div>

                <time>12 min ago</time>
              </div>

              <div className="activity-item">
                <div className="activity-icon">◇</div>

                <div>
                  <strong>
                    Research agent completed
                  </strong>

                  <span>
                    RAG architecture research task
                  </span>
                </div>

                <time>1 hr ago</time>
              </div>

              <div className="activity-item">
                <div className="activity-icon">⌁</div>

                <div>
                  <strong>
                    GitHub connected
                  </strong>

                  <span>
                    Repository integration is ready
                  </span>
                </div>

                <time>Yesterday</time>
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

export default Workspace;