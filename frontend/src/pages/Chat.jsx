import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Brand from "../components/Brand";
import { createConversation } from "../services/conversationService";
import { sendChatMessage } from "../services/chatService";
import "../styles/chat.css";

function Chat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const [conversationId, setConversationId] = useState(null);
  const [loadingConversation, setLoadingConversation] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function initializeConversation() {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setError("You are not logged in.");
        setLoadingConversation(false);
        return;
      }

      try {
        const conversation = await createConversation(token);

        setConversationId(conversation.id);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoadingConversation(false);
      }
    }

    initializeConversation();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || !conversationId || sending) {
      return;
    }

    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("Your session has expired. Please sign in again.");
      return;
    }

    setError("");
    setSending(true);

    const userMessage = {
      role: "user",
      content: trimmedMessage,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setMessage("");

    try {
      const data = await sendChatMessage({
        question: trimmedMessage,
        conversationId,
        token,
      });

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (error) {
      setError(error.message);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "I couldn't process that request. Please try again.",
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  return (
    <main className="chat-page">
      {/* Sidebar */}
      <aside className="chat-sidebar">
        <div>
          <div className="chat-brand">
            <Brand compact />
          </div>

          <button
            className="new-chat-button chat-new-button"
            onClick={() => setMessages([])}
          >
            <span>+</span>
            <span>New conversation</span>
            <kbd>⌘ K</kbd>
          </button>

          <div className="chat-sidebar-section">
            <div className="sidebar-label">CONVERSATIONS</div>

            <button className="conversation active">
              <span className="conversation-icon">✦</span>
              Project research
            </button>

            <button className="conversation">
              <span className="conversation-icon">◌</span>
              RAG architecture
            </button>

            <button className="conversation">
              <span className="conversation-icon">◌</span>
              Weekly planning
            </button>
          </div>

          <div className="chat-sidebar-section">
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

            <Link to="/tools" className="workspace-nav">
              <span>⌁</span>
              Connected tools
            </Link>
          </div>
        </div>

        <Link to="/settings" className="workspace-nav">
          <span>⚙</span>
          Settings
        </Link>
      </aside>

      {/* Chat */}
      <section className="chat-main">
        <header className="chat-header">
          <div>
            <span className="chat-header-title">
              Project research
            </span>

            <span className="chat-header-status">
              <span />
              WorkMind AI
            </span>
          </div>

          <div className="chat-header-actions">
            <button>⌕</button>
            <button>⋯</button>
          </div>
        </header>

        <div className="chat-messages">
          {loadingConversation && (
            <div className="chat-loading">
              Preparing your workspace...
            </div>
          )}

          {error && (
            <div className="chat-error">
              {error}
            </div>
          )}

          {messages.length === 0 ? (
            <div className="chat-empty">
              <div className="chat-empty-icon">✦</div>

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
                    <div className="message-avatar">✦</div>
                  )}

                  <div className="message-content">
                    <span className="message-role">
                      {item.role === "user"
                        ? "You"
                        : "WorkMind"}
                    </span>

                    <p>{item.content}</p>
                  </div>

                  {item.role === "user" && (
                    <div className="message-user-avatar">
                      R
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="chat-composer-area">
          <form
            className="chat-composer"
            onSubmit={handleSubmit}
          >
            <button
              type="submit"
              className="composer-send"
              disabled={
                !message.trim() ||
                !conversationId ||
                sending
              }
            >
              {sending ? "..." : "↑"}
            </button>

            <textarea
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  handleSubmit(event);
                }
              }}
              placeholder="Ask WorkMind anything..."
              rows={1}
            />

            <button
              type="submit"
              className="composer-send"
              disabled={!message.trim()}
            >
              ↑
            </button>
          </form>

          <div className="composer-hint">
            <span>WorkMind can make mistakes.</span>
            <span>Check important information.</span>
          </div>
        </div>
      </section>
    </main>
  );
}

export default Chat;