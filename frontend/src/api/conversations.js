import { api } from "./client";

export function createConversation() {
  return api.post("/conversations/", undefined, {
    errorMessage: "Unable to create conversation.",
  });
}

export function getConversations() {
  return api.get("/conversations/", {
    errorMessage: "Unable to load conversations.",
  });
}

export function deleteConversation(conversationId) {
  return api.delete(`/conversations/${conversationId}`, {
    errorMessage: "Unable to delete conversation.",
  });
}

export function togglePinConversation(conversationId) {
  return api.put(`/conversations/${conversationId}/pin`, undefined, {
    errorMessage: "Unable to update pin status.",
  });
}

export function searchConversations(query) {
  return api.get(`/conversations/search?q=${encodeURIComponent(query)}`, {
    errorMessage: "Unable to search conversations.",
  });
}
