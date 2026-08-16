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