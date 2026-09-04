const API_BASE_URL = "http://localhost:8000";

export async function getConversationMessages(conversationId, token) {
  const response = await fetch(
    `${API_BASE_URL}/messages/${conversationId}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to load conversation messages");
  }

  return response.json();
}