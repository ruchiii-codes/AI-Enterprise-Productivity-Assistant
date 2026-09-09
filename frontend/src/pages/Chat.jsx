import { useEffect, useState } from "react";
import ConversationSearch from "../components/chat/ConversationSearch";
import MessageList from "../components/chat/MessageList";
import Composer from "../components/chat/Composer";
import ConversationList from "../components/chat/ConversationList";
import { Link } from "react-router-dom";
import Brand from "../components/ui/Brand";
import {
  createConversation,
  getConversations,
  deleteConversation,
  togglePinConversation,
  searchConversations,  
} from "../api/conversations";
import { CONVERSATION_STORAGE_KEY } from "../config/env";
import { getConversationMessages } from "../api/messages";
import { sendChatMessage } from "../api/chat";
import { uploadDocument } from "../api/documents";
import { getConversationDocuments } from "../api/documents";
import "../styles/chat.css";
import ProfileMenu from "../components/layout/ProfileMenu";

/**
 * Pinned conversations first, oldest pin first within them, then by id.
 * This comparator was previously duplicated in two handlers.
 */
function sortConversations(a, b) {
  if (a.is_pinned !== b.is_pinned) {
    return a.is_pinned ? -1 : 1;
  }

  if (a.is_pinned && b.is_pinned) {
    return new Date(a.pinned_at) - new Date(b.pinned_at);
  }

  return a.id - b.id;
}

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

      try {
        const existingConversations = await getConversations();

        const conversationsWithMessages = existingConversations.filter(
          (conversation) => conversation.message_count > 0
        );
        
        setConversations(conversationsWithMessages);

        const savedConversationId = localStorage.getItem(
          CONVERSATION_STORAGE_KEY
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
            CONVERSATION_STORAGE_KEY,
            String(selectedConversation.id)
          );

          const previousMessages = await getConversationMessages(
            selectedConversation.id
          );

          setMessages(previousMessages);



          const documents = await getConversationDocuments(
            selectedConversation.id
          );

          setDocuments(documents);
        } else {
          setConversationId(null);
          localStorage.removeItem(CONVERSATION_STORAGE_KEY);
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
  
  
    try {
      setSearching(true);
      setError("");
  
      const results = await searchConversations(trimmedQuery);
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

    try {
      setError("");
      setLoadingConversation(true);

      setConversationId(conversation.id);

      localStorage.setItem(
        CONVERSATION_STORAGE_KEY,
        String(conversation.id)
      );

      const previousMessages = await getConversationMessages(
        conversation.id
      );

      setMessages(previousMessages);

      const conversationDocuments = await getConversationDocuments(
        conversation.id
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


  try {
    await deleteConversation(conversation.id);

    setConversations((prev) =>
      prev.filter((item) => item.id !== conversation.id)
    );

    if (conversation.id === conversationId) {
      setConversationId(null);
      setMessages([]);
      setDocuments([]);
      localStorage.removeItem(CONVERSATION_STORAGE_KEY);
    }
  } catch (error) {
    setError(error.message || "Unable to delete conversation.");
  }
};

  const handleTogglePin = async (conversation) => {
    try {
      const result = await togglePinConversation(conversation.id);

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

        return updated.sort(sortConversations);
      });

      setOpenConversationMenu(null);
    } catch (error) {
      setError(error.message || "Unable to update pin status.");
    }
  };

  const handleNewConversation = async () => {

    try {
      setError("");
      setLoadingConversation(true);

      const conversation = await createConversation();

      const updatedConversations = await getConversations();

      const conversationsWithMessages = updatedConversations.filter(
        (conversation) => conversation.message_count > 0
      );

      const sortedConversations = [...conversationsWithMessages].sort(
        sortConversations
      );

      setConversations(sortedConversations);

      setConversationId(conversation.id);

      localStorage.setItem(
        CONVERSATION_STORAGE_KEY,
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
  
      const result = await uploadDocument(file, conversationId);

      const updatedDocuments = await getConversationDocuments(
        conversationId
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


    setError("");
    setSending(true);

    let currentConversationId = conversationId;

    if (!currentConversationId) {
      try {
        const newConversation = await createConversation();
    
        currentConversationId = newConversation.id;
    
        setConversationId(currentConversationId);
    
        localStorage.setItem(
          CONVERSATION_STORAGE_KEY,
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
      });

      const updatedConversations = await getConversations();

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
      
            <ConversationList
              conversations={conversations}
              activeConversationId={conversationId}
              openMenuId={openConversationMenu}
              onSelect={handleConversationSelect}
              onOpenMenu={setOpenConversationMenu}
              onTogglePin={handleTogglePin}
              onDelete={handleDeleteConversation}
            />

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
          <ConversationSearch
            query={searchQuery}
            results={searchResults}
            searching={searching}
            onQueryChange={handleConversationSearch}
            onSelect={handleSearchResultSelect}
            onClose={() => {
              setSearchOpen(false);
              setSearchQuery("");
              setSearchResults([]);
            }}
          />
        )}

        {/* Messages */}
        <MessageList
          documents={documents}
          messages={messages}
          error={error}
          loadingConversation={loadingConversation}
          sending={sending}
          onSuggestionSelect={setMessage}
        />

        {/* Composer */}
        <Composer
          message={message}
          sending={sending}
          uploading={uploading}
          onMessageChange={setMessage}
          onSubmit={handleSubmit}
          onFileUpload={handleFileUpload}
        />

      </section>
    </main>
  );
}

export default Chat;