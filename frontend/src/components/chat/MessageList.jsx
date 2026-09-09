/**
 * The message transcript: uploaded document chips, error banner, empty state
 * and the rendered conversation.
 *
 * Presentational. onSuggestionSelect fills the composer from the empty-state
 * prompt chips.
 */
import ReactMarkdown from "react-markdown";

export function MessageList({
  documents,
  messages,
  error,
  loadingConversation,
  sending,
  onSuggestionSelect,
}) {
  // The extracted markup calls setMessage for the suggestion chips.
  const setMessage = onSuggestionSelect;

  return (
    <div className="chat-messages">
          
          {documents.length > 0 && (
            <div className="uploaded-documents">
              {documents.map((document) => (
                <div
                  key={document.id}
                  className="uploaded-document"
                >
                  <span className="uploaded-document-icon">📄</span>
          
                  <div className="uploaded-document-info">
                    <span className="uploaded-document-name">
                      {document.filename}
                    </span>
          
                    <span className="uploaded-document-meta">
                      {document.page_count} pages
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
          
            {loadingConversation && (
              <div className="chat-loading">
                <span className="chat-loading-icon">✦</span>
            
                <span>Preparing your workspace</span>
            
                <span className="loading-dots">
                  <i />
                  <i />
                  <i />
                </span>
              </div>
            )}

          {error && (
            <div className="chat-error">
              {error}
            </div>
          )}

          {messages.length === 0 ? (

            <div className="chat-empty">

              <div className="chat-empty-icon">
                ✦
              </div>

              <span className="chat-empty-kicker">
                WORKMIND AI
              </span>

              <h1>
                What can I help
                <br />
                <span>you accomplish?</span>
              </h1>

              <p>
                Ask questions about your knowledge, analyze
                information, or let WorkMind help with a task.
              </p>

              <div className="chat-suggestions">

                <button
                  onClick={() =>
                    setMessage("Explain my RAG architecture")
                  }
                >
                  Explain my RAG architecture
                </button>

                <button
                  onClick={() =>
                    setMessage("Summarize my recent documents")
                  }
                >
                  Summarize my recent documents
                </button>

                <button
                  onClick={() =>
                    setMessage("What should I work on today?")
                  }
                >
                  What should I work on today?
                </button>

              </div>

            </div>

          ) : (

            <div className="message-list">

              {messages.map((item, index) => (

                <div
                  key={index}
                  className={`message-row ${item.role}`}
                >

                  {item.role === "assistant" && (
                    <div className="message-avatar">
                      ✦
                    </div>
                  )}

                  <div className="message-content">

                    <span className="message-role">
                      {item.role === "user"
                        ? "You"
                        : "WorkMind"}
                    </span>

                    <div className="message-markdown">
                      <ReactMarkdown>
                        {item.content}
                      </ReactMarkdown>
                    </div>

                    {item.role === "assistant" && item.sources?.length > 0 && (
                      <div className="message-sources">
                        <div className="message-sources-title">
                          Sources
                        </div>
                    
                        <div className="message-sources-list">
                          {[
                            ...new Map(
                              item.sources.map((source) => [
                                source.filename || source.file_name,
                                source,
                              ])
                            ).values(),
                          ].map((source, sourceIndex) => (
                            <div
                              className="message-source"
                              key={source.filename || source.file_name || sourceIndex}
                            >
                              {source.filename || source.file_name || `Source ${sourceIndex + 1}`}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                  </div>

                  {item.role === "user" && (
                    <div className="message-user-avatar">
                      R
                    </div>
                  )}

                </div>

              ))}

              {sending && (
                <div className="message-row assistant">
                  <div className="message-avatar">
                    ✦
                  </div>
            
                  <div className="message-content">
                    <span className="message-role">
                      WorkMind
                    </span>
            
                    <div className="workmind-thinking">
                      <span>WorkMind is thinking</span>
                      <span className="thinking-dots">
                        <i />
                        <i />
                        <i />
                      </span>
                    </div>
                  </div>
                </div>
              )}

            </div>
          )}

    </div>
  );
}

export default MessageList;
