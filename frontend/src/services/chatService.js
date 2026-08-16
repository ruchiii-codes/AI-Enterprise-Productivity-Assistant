const API_BASE_URL = "http://localhost:8000";

export async function sendChatMessage({
  question,
  conversationId,
  token,
}) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      question,
      conversation_id: conversationId,
    }),
  });

  if (!response.ok) {
    let message = "Something went wrong.";

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