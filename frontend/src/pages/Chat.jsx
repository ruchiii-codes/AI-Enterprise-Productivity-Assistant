import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Brand from "../components/Brand";
import {
  createConversation,
  getConversations,
  deleteConversation,
  togglePinConversation,
  searchConversations,  
} from "../services/conversationService";
import { getConversationMessages } from "../services/messageService";
import { sendChatMessage } from "../services/chatService";
import { uploadDocument } from "../services/uploadService";
import { getConversationDocuments } from "../services/documentService";
import "../styles/chat.css";
import ReactMarkdown from "react-markdown";
import ProfileMenu from "../components/ProfileMenu";

function Chat() {
  const [message, setMessage] = useState("");
  const [documents, setDocuments] = useState([]);
  const [messages, setMessages] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [openConversationMenu, setOpenConversationMenu] = useState(null);

  const [conversationId, setConversationId] = useState(null);
  const [loadingConversation, setLoadingConversation] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    async function initializeChat() {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setError("You are not logged in.");
        setLoadingConversation(false);
        return;
      }

      try {
        const existingConversations = await getConversations(token);

        const conversationsWithMessages = existingConversations.filter(
          (conversation) => conversation.message_count > 0
        );
        
        setConversations(conversationsWithMessages);

        const savedConversationId = localStorage.getItem(
          "workmind_conversation_id"
        );

        let selectedConversation = null;

        // Restore the previously selected conversation
        if (savedConversationId) {
          selectedConversation = conversationsWithMessages.find(
            (conversation) =>
              String(conversation.id) === String(savedConversationId)
          );
        }

        // If saved conversation is unavailable, open the newest conversation
        if (!selectedConversation && conversationsWithMessages.length > 0) {
          selectedConversation = conversationsWithMessages[0];
        }

        if (selectedConversation) {
          setConversationId(selectedConversation.id);

          localStorage.setItem(
            "workmind_conversation_id",
            String(selectedConversation.id)
          );

          const previousMessages = await getConversationMessages(
            selectedConversation.id,
            token
          );

          setMessages(previousMessages);



          const documents = await getConversationDocuments(
            selectedConversation.id,
            token
          );

          setDocuments(documents);
        } else {
          setConversationId(null);
          localStorage.removeItem("workmind_conversation_id");
          setMessages([]);
          setDocuments([]);
        }
        
      } catch (error) {
        setError(error.message);
      } finally {
        setLoadingConversation(false);
      }
    }

    initializeChat();
  }, []);

  const handleConversationSearch = async (query) => {
    setSearchQuery(query);
  
    const trimmedQuery = query.trim();
  
    if (!trimmedQuery) {
      setSearchResults([]);
      return;
    }
  
    const token = localStorage.getItem("access_token");
  
    if (!token) {
      setError("Your session has expired. Please sign in again.");
      return;
    }
  
    try {
      setSearching(true);
      setError("");
  
      const results = await searchConversations(trimmedQuery, token);
      setSearchResults(results);
    } catch (error) {
      setError(error.message || "Unable to search conversations.");
      setSearchResults([]);
    } finally {
      setSearching(false);
    }
  };

  const handleSearchResultSelect = async (conversation) => {
    setSearchOpen(false);
    setSearchQuery("");
    setSearchResults([]);
  
    await handleConversationSelect(conversation);
  };

  const handleConversationSelect = async (conversation) => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("Your session has expired. Please sign in again.");
      return;
    }

    try {
      setError("");
      setLoadingConversation(true);

      setConversationId(conversation.id);

      localStorage.setItem(
        "workmind_conversation_id",
        String(conversation.id)
      );

      const previousMessages = await getConversationMessages(
        conversation.id,
        token
      );

      setMessages(previousMessages);

      const conversationDocuments = await getConversationDocuments(
        conversation.id,
        token
      );
      
      setDocuments(conversationDocuments);

    } catch (error) {
      setError(error.message);
    } finally {
      setLoadingConversation(false);
    }
  };

const handleDeleteConversation = async (conversation) => {
  const confirmed = window.confirm(
    `Delete "${conversation.title || "New Conversation"}"?`
  );

  if (!confirmed) {
    return;
  }

  const token = localStorage.getItem("access_token");

  if (!token) {
    setError("Authentication token not found.");
    return;
  }

  try {
    await deleteConversation(conversation.id, token);

    setConversations((prev) =>
      prev.filter((item) => item.id !== conversation.id)
    );

    if (conversation.id === conversationId) {
      setConversationId(null);
      setMessages([]);
      setDocuments([]);
      localStorage.removeItem("workmind_conversation_id");
    }
  } catch (error) {
    setError(error.message || "Unable to delete conversation.");
  }
};

  const handleNewConversation = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("Your session has expired. Please sign in again.");
      return;
    }

    try {
      setError("");
      setLoadingConversation(true);

      const conversation = await createConversation(token);

      const updatedConversations = await getConversations(token);

      const conversationsWithMessages = updatedConversations.filter(
        (conversation) => conversation.message_count > 0
      );

      const sortedConversations = [...conversationsWithMessages].sort((a, b) => {
        if (a.is_pinned !== b.is_pinned) {
          return a.is_pinned ? -1 : 1;
        }
      
        if (a.is_pinned && b.is_pinned) {
          return new Date(a.pinned_at) - new Date(b.pinned_at);
        }
      
        return a.id - b.id;
      });

      setConversations(sortedConversations);

      setConversationId(conversation.id);

      localStorage.setItem(
        "workmind_conversation_id",
        String(conversation.id)
      );

      setMessages([]);
      setDocuments([]);

    } catch (error) {
      setError(error.message);
    } finally {
      setLoadingConversation(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0];
  
    if (!file) {
      return;
    }
  
    const token = localStorage.getItem("access_token");
  
    if (!token) {
      setError("Your session has expired. Please sign in again.");
      return;
    }
  
    if (file.type !== "application/pdf") {
      setError("Please upload a PDF file.");
      event.target.value = "";
      return;
    }
  
    if (!conversationId) {
      setError("Please create or select a conversation first.");
      event.target.value = "";
      return;
    }
  
    try {
      setError("");
      setUploading(true);
  
      const result = await uploadDocument(file, token, conversationId);

      const updatedDocuments = await getConversationDocuments(
        conversationId,
        token
      );
      
      setDocuments(updatedDocuments);
  
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            `## 📄 Document uploaded successfully!\n\n` +
            `**File:** ${file.name}\n\n` +
            `${result.message || "The document is now available to WorkMind."}`,
        },
      ]);
    } catch (error) {
      setError(error.message);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || sending) {
      return;
    }

    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("Your session has expired. Please sign in again.");
      return;
    }

    setError("");
    setSending(true);

    let currentConversationId = conversationId;

    if (!currentConversationId) {
      try {
        const newConversation = await createConversation(token);
    
        currentConversationId = newConversation.id;
    
        setConversationId(currentConversationId);
    
        localStorage.setItem(
          "workmind_conversation_id",
          String(currentConversationId)
        );
      } catch (error) {
        setError(error.message || "Unable to create conversation.");
        setSending(false);
        return;
      }
    }

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
        conversationId: currentConversationId,
        token,
      });

      const updatedConversations = await getConversations(token);

      const conversationsWithMessages = updatedConversations.filter(
        (conversation) => conversation.message_count > 0
      );

      const sortedConversations = [...conversationsWithMessages].sort((a, b) => {
        if (a.is_pinned !== b.is_pinned) {
          return a.is_pinned ? -1 : 1;
        }
      
        if (a.is_pinned && b.is_pinned) {
          return new Date(a.pinned_at) - new Date(b.pinned_at);
        }
      
        return a.id - b.id;
      });

      setConversations(sortedConversations);

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

      {/* ================= SIDEBAR ================= */}
      <aside className="chat-sidebar">
      
        <div className="chat-sidebar-inner">
      
          {/* Brand */}
          <div className="chat-brand">
            <Brand compact />
          </div>
      
          {/* New conversation */}
          <button
            className="new-chat-button chat-new-button"
            onClick={handleNewConversation}
          >
            <span>+</span>
            <span>New conversation</span>
          </button>
      
          {/* Conversations */}
          <div className="conversations-section">
      
            <div className="sidebar-label">
              CONVERSATIONS
            </div>
      
            <div 
              className="conversation-list"
            >
               
              {console.log(
                "RENDERED CONVERSATIONS:",
                conversations.map((c) => ({
                  id: c.id,
                  title: c.title,
                  is_pinned: c.is_pinned,
                  pinned_at: c.pinned_at,
                }))
              )}
            
              {conversations.map((conversation) => (
                <div
                  key={conversation.id}
                  className={`conversation ${
                    conversation.id === conversationId
                      ? "active"
                      : ""
                  }`}
                  onClick={() =>
                    handleConversationSelect(conversation)
                  }
                >
                  <span className="conversation-icon">
                    {conversation.id === conversationId
                      ? "✦"
                      : "◌"}
                  </span>
      
                  <span className="conversation-title">
                    {conversation.title || "New Conversation"}
                  </span>
                  
                  {conversation.is_pinned && (
                    <span
                      className="conversation-pin-icon"
                      title="Pinned conversation"
                    >
                      📌
                    </span>
                  )}
      
                  <button
                    className="conversation-delete"
                    onClick={(event) => {
                      event.stopPropagation();
                      setOpenConversationMenu(
                        openConversationMenu === conversation.id
                          ? null
                          : conversation.id
                      );
                    }}
                    title="Conversation options"
                  >
                    ⋯
                  </button>

                  {openConversationMenu === conversation.id && (
                    <div
                      className="conversation-menu"
                      onClick={(event) => event.stopPropagation()}
                    >
                      <button
                        className="conversation-menu-item"
                        onClick={async () => {
                          const token = localStorage.getItem("access_token");
                      
                          if (!token) {
                            setError("Authentication token not found.");
                            return;
                          }
                      
                          try {
                            const result = await togglePinConversation(
                              conversation.id,
                              token
                            );
                      
                            setConversations((prev) => {
                              const updated = prev.map((item) =>
                                item.id === conversation.id
                                  ? {
                                      ...item,
                                      is_pinned: result.is_pinned,
                                      pinned_at: result.pinned_at,
                                    }
                                  : item
                              );
                            
                              return updated.sort((a, b) => {
                                if (a.is_pinned !== b.is_pinned) {
                                  return a.is_pinned ? -1 : 1;
                                }
                            
                                if (a.is_pinned && b.is_pinned) {
                                  return new Date(a.pinned_at) - new Date(b.pinned_at);
                                }
                            
                                return a.id - b.id;
                              });
                            });
                      
                            setOpenConversationMenu(null);
                          } catch (error) {
                            setError(error.message || "Unable to update pin status.");
                          }
                        }}
                      >
                        <span>📌</span>
                        <span>
                          {conversation.is_pinned ? "Unpin" : "Pin"}
                        </span>
                      </button>
                  
                      <button
                        className="conversation-menu-item delete"
                        onClick={() => {
                          setOpenConversationMenu(null);
                          handleDeleteConversation(conversation);
                        }}
                      >
                        <span>🗑</span>
                        <span>Delete</span>
                      </button>
                    </div>
                  )}

                </div>
              ))}
      
            </div>

            {conversations.length === 0 && (
              <div className="conversation-empty">
                <span>✦</span>
                <p>No conversations yet</p>
                <small>Start chatting to create one.</small>
              </div>
            )}
            
          </div>
      
          {/* Bottom workspace button */}
          <div className="sidebar-bottom">
            <Link
              to="/workspace"
              className="sidebar-workspace-button"
            >
              <span>▦</span>
              <span>Workspace</span>
            </Link>
          </div>
      
        </div>
      
      </aside>

      {/* ================= MAIN CHAT ================= */}
      <section className="chat-main">

        {/* Header */}
        <header className="chat-header">

          <div className="chat-header-left">
            <span className="chat-header-title">
              WorkMind AI
            </span>

            <span className="chat-header-status">
              <span />
              Online
            </span>
          </div>

          <div className="chat-header-actions">

            {/* Search ONLY on /chat */}
            <button
              className="header-search-button"
              title="Search conversations"
              onClick={() => {
                setSearchOpen(true);
                setSearchQuery("");
                setSearchResults([]);
              }}
            >
              ⌕
            </button>

            {/* User account */}
            <ProfileMenu />

          </div>
        </header>

        {searchOpen && (
          <div
            className="conversation-search-overlay"
            onClick={() => setSearchOpen(false)}
          >
            <div
              className="conversation-search-modal"
              onClick={(event) => event.stopPropagation()}
            >
              <div className="conversation-search-header">
                <span>Search conversations</span>
        
                <button
                  type="button"
                  onClick={() => {
                    setSearchOpen(false);
                    setSearchQuery("");
                    setSearchResults([]);
                  }}
                  title="Close search"
                >
                  ×
                </button>
              </div>
        
              <div className="conversation-search-input-wrapper">
                <span>⌕</span>
        
                <input
                  autoFocus
                  type="text"
                  value={searchQuery}
                  onChange={(event) =>
                    handleConversationSearch(event.target.value)
                  }
                  placeholder="Search your conversations..."
                />
        
                {searching && <span>...</span>}
              </div>
        
              <div className="conversation-search-results">
                {searchQuery.trim() && !searching && searchResults.length === 0 && (
                  <div className="conversation-search-empty">
                    No conversations found.
                  </div>
                )}
        
                {!searchQuery.trim() && (
                  <div className="conversation-search-empty">
                    Search your conversations by title or message.
                  </div>
                )}
        
                {searchResults.map((conversation) => (
                  <button
                    key={conversation.id}
                    type="button"
                    className="conversation-search-result"
                    onClick={() => handleSearchResultSelect(conversation)}
                  >
                    <div className="conversation-search-result-icon">
                      ◌
                    </div>
        
                    <div className="conversation-search-result-content">
                      <div className="conversation-search-result-title">
                        {conversation.title || "New Conversation"}
                      </div>
        
                      {conversation.snippet && (
                        <div className="conversation-search-result-snippet">
                          {conversation.snippet}
                        </div>
                      )}
                    </div>
        
                    {conversation.is_pinned && (
                      <span title="Pinned">📌</span>
                    )}
                  </button>
                ))}
              </div>
      
            </div>
          </div>
        )}

        {/* Messages */}
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

        {/* Composer */}
        <div className="chat-composer-area">

          {uploading && (
            <div className="upload-status">
              <span className="upload-status-icon">↑</span>
              <span>Uploading document...</span>
              <span className="upload-status-dots">
                <i />
                <i />
                <i />
              </span>
            </div>
          )}

          <form
            className="chat-composer"
            onSubmit={handleSubmit}
          >

            <label
              className={`composer-action ${uploading ? "uploading" : ""}`}
              title="Upload document"
            >
              {uploading ? "↑" : "+"}
            
              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleFileUpload}
                disabled={uploading || sending}
                hidden
              />
            </label>

            <textarea
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              onKeyDown={(event) => {
                if (
                  event.key === "Enter" &&
                  !event.shiftKey
                ) {
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
              disabled={
                !message.trim() ||
                sending
              }
            >

              {sending ? "..." : "↑"}
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