const API_BASE_URL = "http://localhost:8000";

export async function getConversationDocuments(
  conversationId,
  token
) {
  const response = await fetch(
    `${API_BASE_URL}/documents/?conversation_id=${conversationId}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch conversation documents.");
  }

  return response.json();
}

export async function getDocuments(token) {
  const response = await fetch(`${API_BASE_URL}/documents/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch documents.");
  }

  return response.json();
}