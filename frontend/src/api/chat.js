import { api } from "./client";

export function sendChatMessage({ question, conversationId }) {
  return api.post(
    "/chat",
    { question, conversation_id: conversationId },
    { errorMessage: "Something went wrong." }
  );
}
