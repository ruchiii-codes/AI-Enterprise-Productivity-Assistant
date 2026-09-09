/**
 * Sidebar list of conversations, each with a pin/delete menu.
 *
 * Presentational: the page owns the data and the handlers.
 */
export function ConversationList({
  conversations,
  activeConversationId,
  openMenuId,
  onSelect,
  onOpenMenu,
  onTogglePin,
  onDelete,
}) {
  // Local aliases so the extracted markup reads unchanged.
  const conversationId = activeConversationId;
  const openConversationMenu = openMenuId;
  const setOpenConversationMenu = onOpenMenu;
  const handleConversationSelect = onSelect;
  const handleTogglePin = onTogglePin;
  const handleDeleteConversation = onDelete;

  return (
    <div className="conversation-list">
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
                        onClick={() => handleTogglePin(conversation)}
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
  );
}

export default ConversationList;
