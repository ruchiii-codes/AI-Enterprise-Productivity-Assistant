import { useCallback, useEffect, useRef, useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import "../styles/workspace.css";
import { getDocuments, uploadDocument } from "../api/documents";

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
  const fetchDocuments = useCallback(async () => {
    try {
      const data = await getDocuments();

      // Cleared after the request resolves so no state is set synchronously
      // during the effect that calls this.
      setError("");
      setDocuments(data);
    } catch (err) {
      setError(
        err.message || "Something went wrong while loading documents."
      );
    } finally {
      setLoadingDocuments(false);
    }
  }, []);

  // Load documents when page opens
  useEffect(() => {
    // fetchDocuments sets state only after awaiting the request, so it cannot
    // cause the cascading render this rule guards against. The rule flags any
    // call to a function containing setState, which is a false positive here.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchDocuments();
  }, [fetchDocuments]);

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
      const data = await uploadDocument(file);

      setMessage(
        data?.message || "Document uploaded and indexed successfully."
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
    <AppLayout status="KNOWLEDGE BASE">
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

                {/* The hidden file input below had no visible trigger, so
                    uploading from this page was unreachable. */}
                <button
                  type="button"
                  className="new-chat-button"
                  onClick={handleUploadClick}
                  disabled={uploading}
                >
                  <span>＋</span>
                  <span>
                    {uploading ? "Uploading..." : "Upload PDF"}
                  </span>
                </button>
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
    </AppLayout>
  );
}

export default Knowledge;