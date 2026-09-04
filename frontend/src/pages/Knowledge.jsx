import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import Brand from "../components/Brand";
import "../styles/workspace.css";
import ProfileMenu from "../components/ProfileMenu";

const API_BASE_URL = "http://localhost:8000";

function Knowledge() {
  const fileInputRef = useRef(null);

  const [documents, setDocuments] = useState([]);
  const [loadingDocuments, setLoadingDocuments] = useState(true);

  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // ---------------------------------------
  // Fetch user's documents
  // ---------------------------------------
  const fetchDocuments = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("Please log in again.");
      setLoadingDocuments(false);
      return;
    }

    try {
      setError("");

      const response = await fetch(`${API_BASE_URL}/documents`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to load your documents."
        );
      }

      setDocuments(data);
    } catch (err) {
      setError(
        err.message || "Something went wrong while loading documents."
      );
    } finally {
      setLoadingDocuments(false);
    }
  };

  // Load documents when page opens
  useEffect(() => {
    fetchDocuments();
  }, []);

  // ---------------------------------------
  // Upload
  // ---------------------------------------
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
        throw new Error(
          "Please log in again before uploading a document."
        );
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

      // Refresh document list after successful upload
      await fetchDocuments();
    } catch (err) {
      setError(
        err.message || "Something went wrong during upload."
      );
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  // ---------------------------------------
  // Format date
  // ---------------------------------------
  const formatDate = (dateString) => {
    if (!dateString) {
      return "Date unavailable";
    }

    const date = new Date(dateString);

    if (Number.isNaN(date.getTime())) {
      return "Date unavailable";
    }

    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

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

            <Link
              to="/knowledge"
              className="workspace-nav active"
            >
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
      </aside>

      {/* Main content */}
      <section className="workspace-main">
        {/* Header */}
        <header className="workspace-header">
          <span className="header-status">
            <span />
            KNOWLEDGE BASE
          </span>

          <div className="header-actions">
            <ProfileMenu />
          </div>
        </header>

        <div className="workspace-content">
          {/* Hero */}
          <section className="workspace-hero">
            <div>
              <span className="hero-kicker">YOUR KNOWLEDGE</span>

              <h1>
                Your documents,
                <br />
                <span>all in one place.</span>
              </h1>

              <p>
                View and manage the documents you’ve added to WorkMind.
              </p>
            </div>
          </section>

          {/* Document count + document list */}
          <section className="knowledge-overview">
            <div className="knowledge-stat">
              <strong>
                {loadingDocuments ? "—" : documents.length}
              </strong>

              <span> Documents uploaded</span>
            </div>

            <div className="knowledge-list-section">
              <div className="knowledge-section-header">
                <span className="card-label">
                  YOUR KNOWLEDGE
                </span>
              </div>

              <div className="knowledge-list">
                {loadingDocuments ? (
                  <div className="knowledge-empty-state">
                    Loading your documents...
                  </div>
                ) : documents.length === 0 ? (
                  <div className="knowledge-empty-state">
                    <span>📄</span>
                    <p>No documents uploaded yet.</p>
                  </div>
                ) : (
                  documents.map((document) => (
                    <div
                      className="knowledge-item"
                      key={document.id}
                    >
                      <div className="knowledge-file">
                        <span className="knowledge-file-icon">
                          📄
                        </span>

                        <div>
                          <h3>{document.filename}</h3>

                          <p>
                            Added{" "}
                            {formatDate(document.created_at)}
                            {" · "}
                            {document.page_count ?? "—"}{" "}
                            {document.page_count === 1
                              ? "page"
                              : "pages"}
                          </p>
                        </div>
                      </div>

                      <span className="knowledge-status">
                        Indexed
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </section>

          {/* Hidden upload input */}
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileChange}
            style={{ display: "none" }}
          />

          {uploading && (
            <p style={{ marginTop: "16px" }}>
              Uploading and indexing document...
            </p>
          )}

          {message && (
            <p style={{ marginTop: "16px" }}>
              {message}
            </p>
          )}

          {error && (
            <p style={{ marginTop: "16px" }}>
              {error}
            </p>
          )}
        </div>
      </section>
    </main>
  );
}

export default Knowledge;