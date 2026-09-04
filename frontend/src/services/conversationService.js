const API_BASE_URL = "http://localhost:8000";

export async function createConversation(token) {
  const response = await fetch(`${API_BASE_URL}/conversations/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    let message = "Unable to create conversation.";

    try {
      const error = await response.json();
      message = error.detail || message;
    } catch {
      // Keep default message
    }

    throw new Error(message);
  }

  return response.json();
}

export async function getConversations(token) {
  const response = await fetch(`${API_BASE_URL}/conversations/`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    let message = "Unable to load conversations.";

    try {
      const error = await response.json();
      message = error.detail || message;
    } catch {
      // Keep default message
    }

    throw new Error(message);
  }

  return response.json();
}

export async function deleteConversation(conversationId, token) {
  const response = await fetch(
    `${API_BASE_URL}/conversations/${conversationId}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    let message = "Unable to delete conversation.";

    try {
      const data = await response.json();
      message = data.detail || data.message || message;
    } catch {
      // Keep default error message
    }

    throw new Error(message);
  }

  return response.json();
}

export async function togglePinConversation(conversationId, token) {
  const response = await fetch(
    `${API_BASE_URL}/conversations/${conversationId}/pin`,
    {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Unable to update pin status.");
  }

  return response.json();
}

export async function searchConversations(query, token) {
  const response = await fetch(
    `${API_BASE_URL}/conversations/search?q=${encodeURIComponent(query)}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    let message = "Unable to search conversations.";

    try {
      const error = await response.json();
      message = error.detail || message;
    } catch {
      // Keep default error message
    }

    throw new Error(message);
  }

  return response.json();
}