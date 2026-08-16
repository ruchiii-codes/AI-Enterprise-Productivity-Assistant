import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import Brand from "../components/Brand";
import "../styles/workspace.css";

const API_BASE_URL = "http://localhost:8000";

function Knowledge() {
  const fileInputRef = useRef(null);

  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setMessage("");
    setError("");

    if (file.type !== "application/pdf") {
      setError("Please select a PDF file.");
      event.target.value = "";
      return;
    }

    setUploading(true);

    try {
      const token = localStorage.getItem("access_token");

      if (!token) {
        throw new Error("Please log in again before uploading a document.");
      }

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/upload/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to upload the document."
        );
      }

      setMessage(
        data.message || "Document uploaded and indexed successfully."
      );
    } catch (err) {
      setError(err.message || "Something went wrong during upload.");
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

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

            <Link to="/knowledge" className="workspace-nav active">
              <span>✦</span>
              Knowledge
            </Link>

            <Link to="/agents" className="workspace-nav">
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
            KNOWLEDGE BASE
          </span>
        </header>

        <div className="workspace-content">
          <section className="workspace-hero">
            <div>
              <span className="hero-kicker">YOUR KNOWLEDGE</span>

              <h1>
                Everything you know,
                <br />
                <span>in one place.</span>
              </h1>

              <p>
                Upload documents, search your knowledge, and get grounded
                answers from your own information.
              </p>
            </div>
          </section>

          <section className="capability-grid">
            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">✦</div>
              </div>

              <div className="card-content">
                <span className="card-label">DOCUMENTS</span>
                <h3>Knowledge library</h3>
                <p>
                  Your indexed documents and enterprise knowledge sources
                  will appear here.
                </p>
              </div>

              <div className="card-metric">
                <strong>39+</strong>
                <span>indexed chunks</span>
              </div>
            </div>

            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">⌕</div>
              </div>

              <div className="card-content">
                <span className="card-label">RETRIEVAL</span>
                <h3>Semantic search</h3>
                <p>
                  Find relevant information using WorkMind&apos;s intelligent
                  retrieval pipeline.
                </p>
              </div>

              <div className="agent-status">
                <span className="pulse-dot" />
                Search ready
              </div>
            </div>

            <div className="dashboard-card">
              <div className="card-top">
                <div className="dashboard-icon">↑</div>
              </div>

              <div className="card-content">
                <span className="card-label">UPLOAD</span>
                <h3>Add knowledge</h3>
                <p>
                  Upload PDF documents to expand your workspace knowledge.
                </p>
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleFileChange}
                style={{ display: "none" }}
              />

              <button
                type="button"
                className="new-chat-button"
                onClick={handleUploadClick}
                disabled={uploading}
              >
                {uploading ? "Uploading..." : "Upload document"}
              </button>

              {message && (
                <p style={{ marginTop: "12px" }}>
                  {message}
                </p>
              )}

              {error && (
                <p style={{ marginTop: "12px" }}>
                  {error}
                </p>
              )}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

export default Knowledge;