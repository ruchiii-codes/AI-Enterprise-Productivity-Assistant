const API_BASE_URL = "http://localhost:8000";

export async function uploadDocument(file, token, conversationId) {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("conversation_id", conversationId);

  const response = await fetch(`${API_BASE_URL}/upload/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!response.ok) {
    let message = "Unable to upload the document.";

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