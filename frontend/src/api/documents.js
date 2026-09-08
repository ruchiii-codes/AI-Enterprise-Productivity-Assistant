import { api } from "./client";

export function getConversationDocuments(conversationId) {
  return api.get(`/documents/?conversation_id=${conversationId}`, {
    errorMessage: "Failed to fetch conversation documents.",
  });
}

export function getDocuments() {
  // Note the trailing slash: "/documents" only worked via a 307 redirect.
  return api.get("/documents/", {
    errorMessage: "Failed to fetch documents.",
  });
}

/**
 * Upload a PDF.
 *
 * `conversationId` is optional: the Knowledge page uploads to the library
 * without a conversation, so the field must be omitted rather than sent as
 * the string "undefined".
 */
export function uploadDocument(file, conversationId) {
  const formData = new FormData();
  formData.append("file", file);

  if (conversationId !== undefined && conversationId !== null) {
    formData.append("conversation_id", conversationId);
  }

  return api.post("/upload/", formData, {
    errorMessage: "Unable to upload the document.",
  });
}
