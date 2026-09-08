import { api } from "./client";

export function getConversationMessages(conversationId) {
  return api.get(`/messages/${conversationId}`, {
    errorMessage: "Failed to load conversation messages.",
  });
}
