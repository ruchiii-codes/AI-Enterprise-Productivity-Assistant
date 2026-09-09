/**
 * Conversation search overlay.
 *
 * Presentational: all state lives in the chat page.
 */
export function ConversationSearch({
  query,
  results,
  searching,
  onQueryChange,
  onSelect,
  onClose,
}) {
  return (
    <div className="conversation-search-overlay" onClick={onClose}>
      <div
        className="conversation-search-modal"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="conversation-search-header">
          <span>Search conversations</span>

          <button type="button" onClick={onClose} title="Close search">
            ×
          </button>
        </div>

        <div className="conversation-search-input-wrapper">
          <span>⌕</span>

          <input
            autoFocus
            type="text"
            value={query}
            onChange={(event) => onQueryChange(event.target.value)}
            placeholder="Search your conversations..."
          />

          {searching && <span>...</span>}
        </div>

        <div className="conversation-search-results">
          {query.trim() && !searching && results.length === 0 && (
            <div className="conversation-search-empty">
              No conversations found.
            </div>
          )}

          {!query.trim() && (
            <div className="conversation-search-empty">
              Search your conversations by title or message.
            </div>
          )}

          {results.map((conversation) => (
            <button
              key={conversation.id}
              type="button"
              className="conversation-search-result"
              onClick={() => onSelect(conversation)}
            >
              <div className="conversation-search-result-icon">◌</div>

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

              {conversation.is_pinned && <span title="Pinned">📌</span>}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ConversationSearch;
